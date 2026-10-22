# WebhookIngest — Reconciliation and Safe Financial Retries

> Part XVI · Chapter 42 · Sections 42.13–42.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Billing State Machine and Reconciliation](../02-deep-dive/02-billing-state-machine-and-reconciliation.md)

## In one sentence

`WebhookIngest` acknowledges events into a durable ledger in milliseconds and lets two
workers — the **applier** and the **reconciliation sweeper** — converge local billing state
onto the provider, while a single **retry classifier** decides what may be retried and with
which key.

## Scenario

Acme receives Stripe webhooks (`WebhookIngest`), applies them to local subscriptions, and
sweeps for drift. Requirements: never double-apply, never trust arrival order, recover missed
events, and never retry a financial write without its idempotency key.

## Part A — The endpoint: verify, ledger, ack

```ts
app.post("/webhooks/stripe", express.raw({ type: "application/json", limit: "1mb" }),
  async (req, res) => {
    if (!verifyStripe(req.body, req.get("Stripe-Signature") ?? "", SECRET)) {
      return res.status(400).json({ error: "invalid_signature" });
    }
    const event = JSON.parse(req.body.toString("utf8")) as StripeEvent;
    try {
      // Ledger insert IS the acknowledgement. Duplicates are primary-key no-ops.
      await db.insert("billing_event_ledger",
        { id: event.id, type: event.type, provider_created: event.created,
          payload: event, state: "received" },
        { onConflict: "id", doNothing: true });
      await queue.enqueue("billing.apply", { eventId: event.id });
      return res.status(200).json({ received: true });
    } catch (err) {
      log.error({ err, eventId: event.id }, "ledger write failed");
      return res.status(503).json({ error: "temporarily_unavailable" }); // sender retries
    }
  });
```

`503` here is deliberate: a failed ledger write must make Stripe retry (up to ~3 days). A
`200` means "recorded," never "applied."

## Part B — The applier worker

```ts
async function applyWorker(eventId: string) {
  const row = await ledger.get(eventId);
  if (!row || row.state !== "received") return;            // duplicate or already applied
  await applyBillingEvent(row.payload);                    // guarded transition, same tx
  await ledger.mark(eventId, "applied");                   // visible progress for support
}
```

Per-event result is recorded; a poison event (schema the projector cannot parse) goes to a
`billing_dlq` with the raw payload, per Chapter 32's rules — **one bad event must not stall
the queue for every tenant**.

## Part C — The reconciliation sweeper

A scheduled job, not a webhook consumer — it works even when webhooks are permanently gone:

```ts
// Nightly: page through local active/past_due subs; compare with provider snapshot.
async function reconcileSweep(cursor?: string) {
  const page = await subs.listActive({ cursor, limit: 100 });
  const providerIds = page.rows.map((s) => s.provider_id);
  const snapshot = await stripeApi.batchRetrieveSubscriptions(providerIds); // rate-limit aware

  for (const local of page.rows) {
    const remote = snapshot.get(local.provider_id);
    if (!remote) {
      await drift.autoResolve(local, "canceled_via_reconciliation"); // provider 404
      continue;
    }
    if (local.status === remote.status) continue;
    const cls = classifyDrift(local, remote);
    if (cls === "provider_ahead_safe")  await drift.autoResolve(local, remote);
    else if (cls === "provider_ahead_money") {
      await drift.autoResolve(local, remote);
      await alerts.page("billing_drift_money", { local, remote }); // refund review
    } else {
      await alerts.page("billing_drift_impossible", { local, remote });
    }
  }
  if (page.nextCursor) await queue.enqueue("billing.reconcile", { cursor: page.nextCursor });
}
```

**Key data:** sweep cadence — **hourly** for `past_due` and top-value cohorts, **nightly**
for all active; auto-apply only drift classes where the provider is definitionally correct
(status, period, plan); anything touching collected money pages a human even when auto-applied.
The sweep itself is a checkpointed batch job: per-item results, partial success tolerated,
the provider's `429` + `Retry-After` honored between pages.

## Part D — One retry classifier for all financial ops

```ts
type RetryDecision =
  | { retry: true;  sameKey: true;  delayMs?: number }   // safe with operation key
  | { retry: false; reason: "terminal" | "action_required" | "bug" }
  | { retry: "reconcile" };                               // ambiguous — park + look up

function classifyPaymentError(err: ProviderError, ctx: { sent: boolean }): RetryDecision {
  switch (err.code) {
    case "rate_limit":
      return { retry: true, sameKey: true, delayMs: err.retryAfterMs ?? 2_000 };
    case "processing_error":
    case "api_error":
      return ctx.sent
        ? { retry: "reconcile" }                          // ambiguous after send
        : { retry: true, sameKey: true };
    case "card_declined": case "expired_card": case "insufficient_funds":
    case "incorrect_cvc":
      return { retry: false, reason: "terminal" };
    case "authentication_required":
      return { retry: false, reason: "action_required" };
    case "invalid_request_error":
      return { retry: false, reason: "bug" };
    case "idempotency_error":
      return err.status === 409
        ? { retry: "reconcile" }                          // concurrent: wait + re-read
        : { retry: false, reason: "bug" };                // key/params misuse
    default:
      return ctx.sent ? { retry: "reconcile" } : { retry: true, sameKey: true };
  }
}
```

Every call site in `Checkout`, the dunning worker, and the refund worker uses this one
function. That is the point: **retry policy for money lives in one reviewed place**, and the
`sameKey` flag is non-negotiable.

```ts
// Call-site pattern: the key travels with the operation, decided before the call.
const decision = classifyPaymentError(err, { sent: attempt.sent });
if (decision.retry === true && decision.sameKey) {
  return retryWithSameKey(order.id, decision.delayMs);    // ledger enforces the key
}
if (decision.retry === "reconcile") {
  await orders.mark(order.id, "pending_verification");
  await queue.enqueue("payment.verify", { orderId: order.id }, { delayMs: 60_000 });
  return;                                                  // never surface as "failed"
}
```

## Real-world use case — the failover weekend

A Postgres failover took `WebhookIngest` down for 25 minutes; Stripe retried, then gave up
on a subset. On Monday: 214 subscriptions said `past_due` while tenants had paid; 6 said
`active` while the provider had canceled them after fraud review. The applier could not help
(events were gone). The nightly sweep — which had been running silently for months — fixed
all 214 with `provider_ahead_safe` auto-apply and paged the 6 money-sensitive cases for
refund review. Mean time to resolution: one sweep, zero manual SQL. The sweep's value was
invisible right up until the moment it was the only thing that worked.

## Trade-offs

| Component | Keep it simple | Add this when |
| --------- | -------------- | ------------- |
| Endpoint | Ledger + enqueue | Always — this *is* the simple version |
| Applier | Single worker | >~50 events/s ⇒ partitioned workers per tenant shard |
| Sweep | Nightly full | Money volume ⇒ hourly cohorts |
| Classifier | Inline switch | Multiple processors ⇒ registry-driven table |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ack into a ledger, apply asynchronously | Apply inline then ack |
| DLQ poison events with raw payload | Let one bad event stall the queue |
| Reconcile even when "webhooks are fine" | Skip the sweep until an incident |
| Centralize money retry policy in one classifier | Reimplement retry logic per call site |
| Page humans for money-sensitive drift | Auto-apply everything |

## Common mistakes

- **Sweep that only compares status strings** — misses period and plan drift.
- **No `state` column on the ledger** — cannot distinguish received/applied/dlq for support.
- **Retry classifier duplicated in three workers** — they drift within a month; one function.
- **Sweep without checkpointing** — a mid-sweep crash restarts from page one and burns API
  quota against rate limits.
- **Treating sweep auto-apply as unreviewable** — every auto-apply writes an audit row.

## Checklist

- [ ] Endpoint returns 2xx only after a durable ledger insert.
- [ ] Duplicate deliveries are primary-key no-ops end to end.
- [ ] Poison events land in a DLQ with payload + error.
- [ ] Reconciliation runs on a schedule even with zero incidents.
- [ ] Drift classes are explicit; money-sensitive drift pages a human.
- [ ] One tested classifier decides every financial retry, always with the operation key.

## Related

- [Checkout Subscription State Machine](./01-checkout-subscription-state-machine.md)
- [Billing State Machine and Reconciliation](../02-deep-dive/02-billing-state-machine-and-reconciliation.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
