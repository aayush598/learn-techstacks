# Refunds, Subscription States, Quotas, and Entitlements

> Part XVI · Chapter 42 · Sections 42.9–42.12 · _Estimated reading time: 22 min_
> **Prerequisite:** [Subscription and Payment Errors](./02-subscription-and-payment-errors.md)

## In one sentence

Refunds can fail for reasons **your code created**, subscription states must move only along
**legal transitions**, and quota/entitlement checks need their own failure policy — because
"the plan table is down" is a decision point, not an exception.

## Why this matters in production

Refund failures usually surface as support escalations: a refund attempted after the charge
left its refundable window, or a refund retried without a key creating duplicate credit-note
requests. Subscription bugs show up as customers stuck in `past_due` forever, or downgraded
mid-cycle because a stale event applied out of order. Quota bugs take two shapes: hard-failing
paid customers when the counter store hiccups, or silently letting an over-limit tenant burn
compute. Each of these is cheap to prevent with a state machine and a defined policy, and
expensive to discover via a customer email.

## 42.9 — Refund failures

A refund is a **new financial operation**, not an "undo." It has its own idempotency key, its
own error surface, and its own irreversibility:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Charge not refundable | Already fully refunded; older than refund window | Terminal; surface "already refunded" as success-shaped state |
| Partial refund over remaining | Math bug / race | Reject before calling provider (`422`) |
| Dispute/chargeback open | Issuer process owns the funds | Terminal; link to dispute workflow — do not also refund |
| Provider transient error | 5xx / network | Retry **with the refund's own idempotency key** |
| Refund succeeds, webhook lost | Async delivery | Local state drifts; reconciliation catches it |

**Key data:** refunds must use their own idempotency key (e.g. `refund:{chargeId}:{n}`) —
reusing the charge's key is a request-mismatch error. Charge refundability is time-boxed by
the processor and card network, **commonly ~60–180 days** depending on the network and
merchant category — check your provider's rule, and treat "outside the window" as terminal.
A refund of an **uncaptured** charge is a cancellation, not a refund — different operation,
different code path.

```ts
async function refundCharge(chargeId: string, amount: number, reason: string) {
  const key = `refund:${chargeId}:${sha256(`${amount}:${reason}`).slice(0, 16)}`;
  //                                    ^^^^^^^^ same intent ⇒ same key ⇒ replay-safe
  try {
    return await stripe.refunds.create({ charge: chargeId, amount, reason }, { idempotencyKey: key });
  } catch (err) {
    if (providerCode(err) === "charge_already_refunded") {
      return existingRefundFor(chargeId, amount);  // idempotent success-shaped outcome
    }
    throw translateToBillingError(err);            // everything else keeps its class
  }
}
```

## 42.10 — Subscription state transitions

Model the subscription as an **explicit state machine**. Legal transitions only; everything
else is a bug or an out-of-order event:

```text
                 ┌──────────▶ canceled ◀──────────┐
                 │               ▲                │
 incomplete ──▶ trialing ──▶ active ──▶ past_due ──┤
     │            │            ▲           │      │
     │            │            └───────────┘      │  (payment retry succeeds)
     ▼            ▼                                │
incomplete_expired (terminal)          unpaid ◀────┘  (retries exhausted)
                                              │
                                              ▼
                                          paused (optional, time-boxed)
```

Rules that make this safe:

1. **Guards, not hope.** Each transition checks `from ∈ allowed_from(to)` and rejects the rest
   with `409 SUBSCRIPTION_INVALID_TRANSITION`.
2. **`canceled` is terminal** for that subscription ID; a new signup creates a new one. Never
   resurrect a canceled row — historical invoices point at it.
3. **Cancel-at-period-end is not canceled.** It is `active` + `cancel_at_period_end: true`;
   entitlements continue until `current_period_end`.
4. **`past_due` is a state, not an error page.** Dunning lives here: the provider retries the
   invoice on its schedule; your job is to warn, gate expensive features if configured, and
   let the webhook drive the next transition.
5. **Timestamps from the provider beat local clocks.** Apply transitions monotonic on the
   provider object's `updated` value (see the deep-dive).

**Key data:** the eight Stripe statuses above are the industry-common vocabulary — even if you
use a different processor, adopting this shape means your mental model transfers. A
recommended grace posture: keep read access through `past_due`, gate writes/expensive
operations after a configurable grace period, hard-gate on `unpaid`/`canceled`.

## 42.11 — Quota enforcement

Quotas ("50 exports/month", "10 GB storage") fail in two special ways:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Race on concurrent usage | Two requests both read count=99, both write 100 | **Atomic** increment/decrement (single DB statement or Lua); never read-modify-write in app code |
| Counter store down | Redis/DB outage | Policy decision: **fail-closed** for expensive/irreversible ops, **fail-open (bounded)** for cheap reads |
| Window rollover bug | Fixed-window boundary double-counts or resets mid-burst | Prefer sliding window or provider-grade limiter for money-adjacent quotas |
| Quota vs billing race | Webhook lag: user upgrades, quota store not yet updated | Serve from entitlement cache with short TTL + force-refresh on upgrade webhook |

The over-consumption window matters: with a monthly quota and an async billing cycle, a tenant
can consume "next month's" allowance before the counter resets. Decide deliberately whether
overage is allowed (usage-based billing) or blocked (hard cap) — and make the error
`429 QUOTA_EXCEEDED` with `Retry-After` for time windows, `402`/`403`-class code with a
purchase CTA for plan caps.

## 42.12 — Entitlement resolution

Entitlements answer "may this tenant use feature X right now?" — and the answer comes from a
**projection of billing state** that can be stale, cached, or down:

| Dependency | Failure | Policy options |
| ---------- | ------- | -------------- |
| Entitlement service down | 5xx/timeout | Cache last-known with TTL; then fail-closed for privileged ops, fail-open for reads if policy allows |
| Cache stale (upgrade just paid) | Lag seconds–minutes | Webhook-triggered cache invalidation; short TTL (commonly 1–5 min) for money-adjacent features |
| Feature flag + entitlement both read | One says yes, one says no | Entitlement is authoritative; flags gate rollout, never entitlement |
| Mid-cycle downgrade | Event out of order | Entitlement derived from projected state with monotonic guards |

```ts
async function assertEntitlement(tenantId: string, feature: Feature): Promise<void> {
  try {
    const e = await entitlements.get(tenantId, feature, { maxAgeMs: 60_000 });
    if (!e.granted) throw new EntitlementMissing({ feature, plan: e.plan }); // 403-class
  } catch (err) {
    if (isEntitlementServiceUnavailable(err)) {
      // Expensive/irreversible operations MUST fail closed on unknown entitlements.
      if (FEATURES[feature].costly) throw EntitlementUnverifiable({ feature }); // 503-class
      // Cheap reads may ride a stale cache; without one, fail closed too.
      const fallback = await entitlements.lastKnown(tenantId, feature);
      if (fallback?.granted) return;                                            // degraded OK
      throw EntitlementUnverifiable({ feature });
    }
    throw err;
  }
}
```

**Key data:** recommended entitlement cache TTL **1–5 minutes** for money-adjacent features,
with webhook-driven invalidation to shrink the upgrade lag to near zero. The decision matrix
"fail-open vs fail-closed per feature" is the same idea as Chapter 30's degradation rules,
applied to money.

## Worked example — Acme entitlement drift

Acme's `past_due` grace logic gated exports in app code with `if (subscription.status !==
"active")`. A customer who upgraded from Starter to Pro mid-cycle had a webhook land while the
export worker pool was saturated; the `subscription.updated` event applied 40 minutes late, and
for those 40 minutes exports were rejected with a confusing `403`. Worse, a second, older
`invoice.paid` event arrived *after* the upgrade event and **downgraded** the local projection
back to Starter — the applier had no monotonic guard. Fixes: (1) transitions guarded by the
provider object's `updated` timestamp; (2) cache invalidation on the upgrade webhook;
(3) entitlement failures on the export path return `503`-class "try again shortly," not a
permanent-sounding `403` — because the entitlement was *unverifiable*, not *missing*.

## Trade-offs

| Decision | Fail-open | Fail-closed |
| -------- | --------- | ----------- |
| Cheap read of cached data | Availability preserved; tiny overuse risk | Outages cascade to users |
| Expensive compute (exports, LLM calls) | Cost runaway during outages | Some users blocked briefly |
| Irreversible action (send email, charge) | Fraud/abuse risk | Correct default |
| Admin-only operation | — | Always closed |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give refunds their own idempotency key | Reuse the charge's key |
| Guard every subscription transition | Trust that events arrive in order |
| Atomically consume quota | Read-modify-write counters in app code |
| Distinguish "entitlement missing" from "unverifiable" | Return 403 for an entitlement outage |
| Fail closed for costly ops on unknown entitlement | Fail open everywhere "for availability" |

## Common mistakes

- **Refund without a key** — provider retries create duplicate refund requests.
- **Treating `cancel_at_period_end` as canceled** — paying customers locked out early.
- **Non-atomic quota decrement** — oversell under concurrency, always at the worst moment.
- **`403` for a downed entitlement service** — clients cache the denial; users stay locked out
  after recovery.
- **App-code entitlement checks that ignore the projection** — every feature invents its own
  stale read.

## Checklist

- [ ] Refunds are idempotent and handle "already refunded" as success-shaped.
- [ ] Subscription transitions go through one guarded state machine.
- [ ] Quota consumption is atomic in the store, not in application memory.
- [ ] Entitlement outages are distinguishable (503-class) from missing entitlements (403-class).
- [ ] Costly/irreversible operations fail closed when entitlements are unverifiable.
- [ ] Upgrade webhooks invalidate entitlement caches.

## Related

- [Invoice, Webhooks, and Billing Consistency](./04-invoice-webhooks-and-billing-consistency.md)
- [Entitlement Resolution and Quota Mechanics](../02-deep-dive/03-entitlement-resolution-and-quota-mechanics.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
