# Checkout and Webhook Idempotency

> Part XI · Chapter 28 · Sections 28.11–28.13, 28.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Idempotency in Payments, Jobs, and Webhooks](../01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md)

## In one sentence

This is the **two-end safety net** for money: `Checkout` sends a stable key to both its own store and
the payment provider, and `WebhookIngest` dedupes provider events by event id before applying any
state change.

## Why this matters in production

Payments fail at the seams. The client retries, the API retries the provider, the provider retries
the webhook — each is a chance to charge twice or transition a subscription twice. The two ends have
different natural keys (an order key for the charge, an event id for the webhook), and both must be
enforced. If either end is missing, the other cannot save you.

## Checkout — charge idempotency

### Key derivation

```text
charge_key = `${tenantId}:${orderId}:charge`
refund_key = `${tenantId}:${paymentId}:refund:${refundRequestId}`
```

Deterministic: a retried checkout reproduces the same key. The client never invents a new key on
retry.

### Server-side flow

```ts
export async function payOrder(tenantId: string, orderId: string, reqId: string) {
  const order = await orders.get(tenantId, orderId);
  if (!order) return problem(404, "ORDER_NOT_FOUND");
  if (order.status === "paid") return replayPaid(order);

  const key = `${tenantId}:${orderId}:charge`;
  const payload = { orderId, amount: order.amount, currency: order.currency };

  const claim = await store.claim(tenantId, key, payload, reqId);
  if (!claim.claimed) return claim.replay;

  try {
    const charge = await stripe.charges.create(
      {
        amount: order.amount,        // server-side amount, never the client's
        currency: order.currency,
        customer: order.customerId,
        metadata: { order_id: orderId, tenant_id: tenantId },
      },
      { idempotencyKey: key },       // SAME key at the provider
    );

    await db.transaction(async (tx) => {
      await tx.update("orders", orderId, { status: "paid", charge_id: charge.id });
      await tx.query(
        `UPDATE idempotency_keys
            SET state='completed', status_code=201,
                response_body=$3, resource_id=$4, lease_until=NULL
          WHERE tenant_id=$1 AND key=$2`,
        [tenantId, key, { orderId, chargeId: charge.id, status: "paid" }, charge.id],
      );
    });

    return json(201, { orderId, chargeId: charge.id, status: "paid" });
  } catch (err) {
    if (isTerminalPaymentError(err)) {
      await store.fail(tenantId, key, "terminal", 402, { code: err.code }, err.code);
      return problem(402, err.code);
    }
    // Provider timeout: the charge may exist.
    await store.markUnknown(tenantId, key, String(err));
    return problem(503, "PAYMENT_OUTCOME_UNKNOWN", { retryAfterMs: 2_000 });
  }
}
```

### Refunds

```ts
const refundKey = `${tenantId}:${paymentId}:refund:${refundRequestId}`;
await stripe.refunds.create(
  { charge: payment.providerChargeId, amount: refundAmount },
  { idempotencyKey: refundKey },
);
```

A retried refund request returns the original refund instead of creating a second one. `refundRequestId`
is generated once when the operator opens the refund form, not per click.

### Reconciliation

```ts
async function reconcileUnknownPayments() {
  const rows = await store.listByState("unknown", { limit: 100 });
  for (const row of rows) {
    const found = await stripe.charges.search({
      query: `metadata['order_id']:'${row.resourceId}'`,
    });
    if (found.data.length === 1) {
      await store.complete(row.tenantId, row.key, 201, toPaidBody(found.data[0]),
                           found.data[0].id);
    } else if (Date.now() - row.createdAt > 10 * 60_000) {
      await store.fail(row.tenantId, row.key, "retryable", undefined, undefined,
                       "not found at provider after 10m");
    }
  }
}
```

## WebhookIngest — event idempotency

### The endpoint

```ts
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), async (req, res) => {
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      req.body, req.header("stripe-signature")!, process.env.STRIPE_WEBHOOK_SECRET!,
    );
  } catch (err) {
    return res.status(400).json({ error: "invalid_signature" });
  }

  // Dedup BEFORE acknowledging or processing.
  const inserted = await events.insertIfAbsent({
    provider: "stripe",
    eventId: event.id,           // evt_...
    type: event.type,
    payloadHash: canonicalHash(event.data.object),
    receivedAt: new Date(),
  });

  if (!inserted) {
    return res.status(200).json({ received: true, duplicate: true });
  }

  // Acknowledge fast; process asynchronously.
  await queue.enqueue("stripe-events", {
    eventId: event.id,
    type: event.type,
    payload: event.data.object,
  });

  return res.status(200).json({ received: true });
});
```

### The worker

```ts
queue.process("stripe-events", async (job) => {
  // The queue is at-least-once; dedupe again at the effect boundary.
  const applied = await appliedEvents.claim(job.data.eventId);
  if (!applied) return; // already processed

  switch (job.data.type) {
    case "invoice.paid":
      await billing.markPaidIdempotent(job.data.payload);
      break;
    case "customer.subscription.deleted":
      await subscriptions.cancelIdempotent(job.data.payload.id);
      break;
    default:
      await appliedEvents.markIgnored(job.data.eventId);
  }

  await appliedEvents.complete(job.data.eventId);
});
```

### Event dedup table

```sql
CREATE TABLE webhook_events (
  provider    text        NOT NULL,
  event_id    text        NOT NULL,
  type        text        NOT NULL,
  payload_hash text       NOT NULL,
  state       text        NOT NULL DEFAULT 'received',
  received_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (provider, event_id)
);
```

`INSERT ... ON CONFLICT DO NOTHING` returns zero rows for duplicates — the same atomic pattern as the
idempotency store.

## Why two layers

| Layer | Protects against | Key |
| ----- | ---------------- | --- |
| Checkout store | Client/API retries, double-click | `tenant:order:charge` |
| Provider key | Network ambiguity between you and Stripe | Same key |
| Webhook event store | Provider redelivery and your own queue retries | `evt_...` |
| Effect-level claim | Queue redelivery | `evt_...` or derived |

No single layer covers all four duplicate sources, which is why the design uses all of them.

## Worked example — duplicate invoice event

```text
1. Stripe sends invoice.paid evt_1. We insert evt_1, enqueue, return 200.
2. Worker marks evt_1 applied, updates invoice, sends receipt.
3. Stripe redelivers evt_1 (didn't see our 200 in time).
4. Endpoint insertIfAbsent(evt_1) → duplicate → 200 {duplicate:true}.
5. No second enqueue, no second receipt.
```

## Key data / numbers

- Stripe idempotency-key retention: **24 hours** by default.
- Stripe webhook event ids: `evt_...`, globally unique per account.
- Webhook response target: **under a few seconds**; queue long work.
- Reconciliation lookback: **10 minutes** minimum for provider charge search.
- `Idempotency-Key` pass-through: same string to your DB and the provider.
- Duplicate webhook status: `200`, body `{ "duplicate": true }`.

## Real-world use case — Checkout + WebhookIngest

Checkout had both a key at its own store and a Stripe key, but `WebhookIngest` did not dedupe. During
a network partition, Stripe redelivered `invoice.paid` four times; the handler sent four receipts and
created four accounting entries. After adding the `webhook_events` table keyed by `evt_...` and a
second claim in the worker, duplicate effects stopped. The two layers now cover both directions:
outbound retries (order key) and inbound redelivery (event id).

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Dedup in endpoint | Fast, simple | Still need effect-level dedup |
| Dedup only in worker | Endpoint stays thin | Duplicate enqueues |
| Dedup both | Strongest | Slightly more storage |
| Provider key only | Simple | No protection for local writes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive the charge key from the order | Generate a key per button click |
| Pass the same key to the provider | Use a different provider key |
| Dedup webhooks on event id | Dedup on payload body |
| Return `200` for duplicates | Return `409` and trigger more retries |
| Ack webhooks before long work | Process synchronously |
| Reconcile unknown charges | Mark them failed and move on |

## Common mistakes

- **Trusting a client-supplied amount** on a retried request.
- **Generating the refund key per click**, double-refunding.
- **Deduping webhooks after processing**, so the first duplicate already applied.
- **Returning `500` to a duplicate webhook**, causing infinite redelivery.
- **No effect-level dedup**, so queue redelivery re-applies the event.

## Checklist

- [ ] Charge key derived from tenant + order.
- [ ] Same key passed to the provider.
- [ ] Refund key derived from the refund request.
- [ ] Unknown charges are reconciled, not failed.
- [ ] Webhooks verified before dedup.
- [ ] Webhooks deduped on event id before processing.
- [ ] Endpoint returns `2xx` for duplicates.
- [ ] Worker re-claims the event id before applying effects.

## Related

- [Idempotency in Payments, Jobs, and Webhooks](../01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md)
- [Failure Contracts and Uncertain Outcomes](../01-concepts/03-failure-contracts-and-uncertain-outcomes.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 42 — Authentication, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
