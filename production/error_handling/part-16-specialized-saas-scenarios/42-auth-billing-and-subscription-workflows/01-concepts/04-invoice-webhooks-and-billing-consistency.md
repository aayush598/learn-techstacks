# Invoices, Webhook-Driven State, and Billing Consistency

> Part XVI · Chapter 42 · Sections 42.13–42.15 · _Estimated reading time: 20 min_
> **Prerequisite:** [Refunds, Subscription States, Quotas, and Entitlements](./03-refunds-subscription-states-and-entitlements.md)

## In one sentence

Invoices fail asynchronously, billing state arrives by webhook **duplicated, reordered, and
sometimes not at all**, so your local projection must be an idempotent, monotonic applier with
a **reconciliation job** as the backstop that eventually makes local match the provider.

## Why this matters in production

The billing database is a *projection* of what the payment provider knows. Treat it as the
source of truth and three bugs follow within a quarter: a replayed `invoice.paid` credits a
tenant twice; an `invoice.payment_failed` that arrives before the subscription row exists is
dropped and the tenant is never downgraded; a missed `customer.subscription.updated` leaves a
churned tenant with Pro entitlements for months. None of these throw exceptions — they are
silent state corruption, which is the most expensive class of billing bug.

## 42.13 — Invoice generation

Invoices are generated and settled asynchronously by the provider. Your failure surface:

| Failure | Cause | Correct outcome |
| ------- | ----- | ------------------- |
| Invoice finalization failed | Tax engine / provider error | Retry per provider schedule; notify tenant on terminal failure |
| Tax calculation provider down | Third-party outage | Do not finalize with wrong tax; hold the invoice, alert |
| Payment on invoice fails | Declined card | `past_due` + dunning sequence; **not** an exception in your request path |
| Invoice voided/updated | Credit, plan change | Apply the event; local projection must accept invoice *updates*, not just creation |
| Webhook for the invoice lost | Provider retry exhausted / endpoint down | Reconciliation finds the drift (below) |

Dunning — the retry-and-notify sequence for a failed invoice payment — is **provider-driven**
by default. Configure it deliberately: how many retries, over what schedule, what happens at
exhaustion (`unpaid` or `canceled`), and which in-app banners correspond to `past_due`. A
commonly safe default is a handful of retries over days to weeks with a clear in-product
warning from the first failed attempt, because customers fix cards when they see the banner.

## 42.14 — Webhook-driven billing state

`WebhookIngest` receives events; a projector turns them into local state. The three
transport facts you must design for (Chapter 33 covers the mechanics):

1. **Duplicates.** Stripe retries failed deliveries for up to **~3 days**. Every applier run
   for the same `event.id` must be a no-op the second time.
2. **Reordering.** Two events for the same subscription can arrive in either order. An older
   `invoice.paid` must not overwrite a newer `subscription.updated`.
3. **Loss.** A endpoint outage longer than the retry window means events are **gone**. Only
   reconciliation can recover those.

```ts
// The applier contract: idempotent, monotonic, transactional.
async function applyBillingEvent(event: StripeEvent): Promise<void> {
  await db.transaction(async (tx) => {
    const inserted = await tx.insertIgnore("billing_event_ledger", {
      id: event.id,                      // PRIMARY KEY → duplicates are no-ops
      type: event.type,
      created: event.created,
      payload: event,
    });
    if (!inserted) return;               // duplicate delivery: stop here

    const obj = extractSubscriptionProjection(event); // null for irrelevant types
    if (!obj) return;

    const current = await tx.getSubscriptionForUpdate(obj.providerId);
    if (current && obj.providerUpdatedAt < current.provider_updated_at) {
      return;                            // stale/out-of-order: ignore, keep newer state
    }
    await tx.updateSubscription(obj.providerId, {
      status: obj.status,
      provider_updated_at: obj.providerUpdatedAt,
      version: current.version + 1,      // optimistic concurrency for readers
    });
  });
}
```

**Key data:** dedupe key = provider `event.id` (Stripe: `evt_...`); monotonic guard = the
provider object's `updated` timestamp (Stripe: `created` on the object, or
`current_period_end` for period-sensitive transitions); ack fast (`200` after ledger insert),
process in a worker — the full endpoint pattern is in Chapter 33.

## 42.15 — Preventing inconsistent billing state

Defense in depth, cheapest first:

1. **One applier, one ledger.** All billing state changes flow through the idempotent applier.
   No feature team writes `subscriptions.status` directly — that is how drift gets seeded.
2. **Transactional outbox.** When local state changes, emit the domain event
   (`SubscriptionUpgraded`) from the same transaction, so entitlement caches invalidate even
   if the process dies right after the commit.
3. **Reconciliation job.** Nightly (or hourly for high-value accounts), compare local
   projections against provider objects; classify drift; auto-apply safe fixes; alert on the
   rest.
4. **Redirects are not proof.** After checkout redirect, *retrieve* the session server-side
   before granting anything, or simply wait for the webhook.
5. **Append-only audit.** Every billing state change writes an audit row (who/what/when/why)
   so a support question is a query, not a log archaeology dig.

```sql
-- Drift detection: local vs provider is a nightly query, not a mystery.
SELECT s.id, s.status AS local_status, p.status AS provider_status, s.updated_at
FROM subscriptions s
JOIN provider_subscription_snapshot p ON p.provider_id = s.provider_id
WHERE s.status IS DISTINCT FROM p.status
  AND p.fetched_at > now() - interval '1 hour';
```

**Key data:** reconciliation cadence recommendation — **hourly** for subscription status on
paid plans, **nightly** minimum; auto-apply only monotonic, provider-wins fixes (provider is
the source of truth for billing), and page a human for anything involving money already
collected (status says `active`, provider says `canceled` — check for a refund owed).

## Worked example — WebhookIngest drift that cost an upgrade

Acme's projector processed events inline and acked with `200` only after the update. During a
Postgres failover, the endpoint returned `503` for ~25 minutes; Stripe retried but eventually
exhausted. Result: 214 subscriptions whose `invoice.paid` was never applied — tenants paid,
local state said `past_due`, entitlements were gated. The fix: (1) ack-after-ledger-insert
pattern so a `200` means "recorded"; (2) nightly reconciliation job comparing
`subscriptions` to a provider snapshot; the first run found and fixed all 214 rows; (3) an
alert on drift count > 0 for `active`/`canceled` mismatches. The outage was identical; the
*recoverability* was new.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Webhook-only | Simple | Event loss = permanent drift | Toys, not billing |
| Webhook + nightly reconciliation | Self-healing | Extra job + snapshot API calls | ✅ Default |
| Poll-only (no webhooks) | No inbound surface | Lag, API quota burn | Very low volume |
| Inline apply + ack | Immediate state | Timeouts duplicate; slow acks | Never for billing |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Store every event in a ledger keyed by `event.id` | Process the same delivery twice |
| Guard transitions with provider timestamps | Assume arrival order equals event order |
| Reconcile against the provider on a schedule | Trust the local projection forever |
| Retrieve the session server-side after redirect | Grant entitlements on redirect alone |
| Write billing changes through one applier | UPDATE subscriptions.status from feature code |

## Common mistakes

- **No event ledger** — dedupe via "check current status" accidentally skips legitimate
  repeated events (e.g. two `invoice.paid` for two invoices).
- **Last-write-wins applier** — an old event silently regresses a newer state.
- **Reconciliation that only alerts** — drift is found but nobody fixes it; auto-apply the
  safe class.
- **Trusting the success redirect** — the most common source of "paid but no access."
- **Feature-code writes to billing tables** — projection and source of truth get confused.

## Checklist

- [ ] All billing state changes go through one idempotent applier.
- [ ] The event ledger's primary key is the provider `event.id`.
- [ ] Appliers compare provider timestamps and ignore stale events.
- [ ] A reconciliation job exists and its first run has been allowed to find real drift.
- [ ] Checkout redirects are verified server-side or ignored in favor of webhooks.
- [ ] Billing changes emit outbox events for cache invalidation.

## Related

- [Billing State Machine and Reconciliation](../02-deep-dive/02-billing-state-machine-and-reconciliation.md)
- [Webhook Reconciliation and Safe Financial Retries](../03-practical-examples/02-webhook-reconciliation-and-safe-financial-retries.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
