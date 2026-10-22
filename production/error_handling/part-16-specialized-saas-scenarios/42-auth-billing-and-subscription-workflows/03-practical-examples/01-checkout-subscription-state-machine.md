# Checkout — Subscription State Machine End to End

> Part XVI · Chapter 42 · Sections 42.5, 42.8, 42.10 · _Estimated reading time: 24 min_
> **Prerequisite:** [Ambiguous Payment Outcomes and Idempotency](../02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md)

## In one sentence

This example wires the pieces together: a server-minted idempotency key, a PaymentIntent that
may return `requires_action`, a subscription state machine, and a webhook applier — so that
double-clicks, 3DS challenges, and timeouts all land in a **defined state**.

## Scenario

`Checkout` sells Acme SaaS Pro at $49/mo. The browser is untrusted, the network is flaky, and
Stripe is the processor. Every outcome below must end in a state the UI can render and the
billing database can defend.

## Step 1 — Create the intent (server-side, key minted once)

```ts
// POST /api/checkout/sessions — called when the checkout page loads.
async function createCheckoutSession(tenantId: string, plan: PlanId) {
  const order = await orders.insert({ tenantId, plan, amount: PLAN_PRICE[plan],
    status: "pending_payment" });                    // committed BEFORE the provider call
  const key = `checkout:${order.id}`;                // operation-scoped key

  const intent = await stripe.paymentIntents.create(
    { amount: order.amount, currency: "usd",
      metadata: { orderId: order.id, tenantId } },   // metadata = reconciliation handle
    { idempotencyKey: key },
  );

  await ledger.put(key, { orderId: order.id, requestHash: hash(order),
    providerId: intent.id, status: "in_flight" });
  return { orderId: order.id, clientSecret: intent.client_secret };
}
```

Why this order: the order row exists before the provider call, so even a crash between the
two leaves a recoverable `pending_payment` row the reconciliation worker can find via
`metadata.orderId`.

## Step 2 — Client confirmation and the `requires_action` fork

The browser confirms the PaymentIntent with the card element. Three results, three client
behaviors — and the server is the arbiter of all of them:

```ts
// Client (simplified). The server never trusts this outcome; it is a UX hint only.
try {
  const r = await stripe.confirmPayment({ clientSecret, redirect: "if_required" });
  if (r.paymentIntent.status === "requires_action") {
    showThreeDS(r.paymentIntent.next_action);        // card issuer challenge
  } else {
    redirectToApp();                                 // server still waits for webhook
  }
} catch (err) {
  if (err.code === "card_declined") showUpdateCard();  // terminal, actionable
  else showRetrySameKey();                             // transient: same order/key
}
```

`authentication_required` / `requires_action` is **not a failure**. The subscription sits in
`incomplete` with `pending_payment_state: requires_action`; the UI shows "complete your bank
verification." Confusing this with a decline is the most common checkout UX bug.

## Step 3 — The state machine as code

```ts
const TRANSITIONS: Record<SubStatus, Partial<Record<SubStatus, true>>> = {
  incomplete:        { trialing: true, active: true, incomplete_expired: true, canceled: true },
  trialing:          { active: true, past_due: true, canceled: true },
  active:            { past_due: true, paused: true, canceled: true },
  past_due:          { active: true, unpaid: true, canceled: true },
  paused:            { active: true, canceled: true },
  unpaid:            { active: true, canceled: true },
  canceled:          {},                                 // terminal
  incomplete_expired:{},                                 // terminal
};

function transition(row: SubscriptionRow, to: SubStatus, event: StripeEvent): void {
  if (TERMINAL.has(row.status))
    throw new BillingError("SUBSCRIPTION_TERMINAL", { current: row.status });
  if (!TRANSITIONS[row.status]?.[to])
    throw new BillingError("SUBSCRIPTION_INVALID_TRANSITION", { from: row.status, to });
  if (event.createdObjectTime <= row.provider_updated_at)
    return;                                              // stale: no-op, metric only
  applyRow(row, to, event);                              // same tx as ledger insert
}
```

## Step 4 — Webhook applier closes the loop

The webhook, not the redirect, is what moves the subscription to `active`:

```ts
// Events that matter to Checkout (subscribe to exactly these; ignore the rest).
const HANDLED = new Set([
  "checkout.session.completed",
  "customer.subscription.updated",
  "customer.subscription.deleted",
  "invoice.payment_failed",
  "invoice.paid",
]);

async function onStripeEvent(event: StripeEvent) {
  if (!HANDLED.has(event.type)) return;                  // narrow surface
  await apply(event);                                    // ledger + guarded transition
  if (event.type === "customer.subscription.updated") {
    await outbox.emit("subscription.changed", extract(event)); // cache invalidation
  }
}
```

## Outcome matrix — every path lands somewhere

| Path | Order status | Subscription status | UI |
| ---- | ------------ | ------------------- | -- |
| Card succeeds first try | `paid` (webhook) | `active` | Welcome |
| 3DS required, completed | `paid` (webhook) | `active` | "Verifying…" → Welcome |
| 3DS required, abandoned | `pending_payment` | `incomplete` → `incomplete_expired` | "Complete verification" / session expired |
| Card declined | `pending_payment` | `incomplete` | Update card CTA |
| Timeout on confirm (ambiguous) | `pending_verification` | `incomplete` | "Confirming payment…" — **not** "failed" |
| Webhook lost entirely | `pending_payment` | `incomplete` | Reconciliation finds charge via metadata → force-apply |
| Double-click on pay | same order, same key | single subscription | Provider replays; no second charge |

**Key data:** idempotency key = `checkout:{orderId}` (operation-scoped, retained locally
indefinitely, provider-side 24 h); reconciliation handle = `metadata.orderId` on every
provider object; Stripe statuses modeled: PaymentIntent `requires_action`/`processing`/
`succeeded` and Subscription `incomplete`/`active`/`incomplete_expired`.

## Failure-path walkthroughs

**Timeout mid-confirm.** Client shows "confirming." Server marks the order
`pending_verification`; the verification worker replays with the same key (safe within 24 h)
or searches by `metadata.orderId`. If the charge exists: apply `active`, done. If the provider
confirms nothing after backoff: `failed_definite`, show update-card. The user is never told
"failed" while money might have moved.

**Webhook arrives before the local subscription row.** The applier upserts a shell row keyed
on `provider_id` — the checkout flow's later write reconciles via the same key. No dropped
event, no manual SQL.

**Late `invoice.paid` after cancel.** Terminal-state guard rejects the transition; the invoice
projection still records the payment (refunds are a separate operation, section 42.9).

## Real-world use case — Acme's launch

At launch, Acme's older flow minted a key per HTTP request. 1.4% duplicate-charge rate,
visible within a day. After the rewrite above: same-key replays collapsed retries;
`requires_action` got its own UI (support tickets about "declined but my bank says fine"
dropped to zero); `pending_verification` plus metadata-based reconciliation resolved all
timeout cases without a single manual refund in the following quarter.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Commit the order before calling the provider | Call the provider first, then persist |
| Key by `checkout:{orderId}` | Key by request UUID |
| Wait for the webhook before granting | Trust the client redirect |
| Give `requires_action` its own state and UI | Collapse it into "declined" |
| Park ambiguous outcomes for reconciliation | Auto-fail them |

## Checklist

- [ ] Order row is committed before the provider call.
- [ ] Idempotency key is derived from the order ID everywhere.
- [ ] `requires_action` renders a challenge flow, not an error.
- [ ] Only the webhook (or a server-side retrieve) flips `pending_payment → paid`.
- [ ] State machine rejects illegal and stale transitions.
- [ ] Every row of the outcome matrix has a UI state and an owner.

## Related

- [Ambiguous Payment Outcomes and Idempotency](../02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md)
- [Webhook Reconciliation and Safe Financial Retries](./02-webhook-reconciliation-and-safe-financial-retries.md)
- [Subscription and Payment Errors](../01-concepts/02-subscription-and-payment-errors.md)
- [Chapter 42 Reference](../05-reference/README.md)
