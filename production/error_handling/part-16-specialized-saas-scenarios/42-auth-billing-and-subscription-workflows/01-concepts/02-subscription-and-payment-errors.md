# Subscription and Payment Errors — Creation, Provider Codes, Duplicates, Ambiguity

> Part XVI · Chapter 42 · Sections 42.5–42.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Account Lifecycle Errors](./01-account-lifecycle-errors.md)

## In one sentence

Payment failures must be classified into **terminal** (declined — never retry), **action-
required** (3DS/SCA — not a failure at all), and **transient** (retry with the *same*
idempotency key), and a timeout on a charge is an **ambiguous outcome** you reconcile, not a
failure you blindly retry.

## Why this matters in production

A `card_declined` treated as transient gets retried and retries hammer the issuer, annoy the
customer, and can create partial states. A timeout treated as "failed" gets re-submitted and
**double-charges the customer** — the single most trust-destroying billing bug there is. And a
subscription created without modeling `incomplete` / `requires_action` leaves customers who
successfully started checkout in a state your app cannot describe. This file gives you the
error taxonomy; the deep-dive gives you the resolution mechanics.

## 42.5 — Subscription creation

A subscription is **not** created when the customer clicks "Subscribe." It is created in a
pending state and only becomes active when the first payment succeeds:

```text
Checkout session created
      │
      ▼
subscription: incomplete ──payment succeeded──▶ active (or trialing)
      │
      ├─payment requires 3DS──▶ incomplete + requires_action  (NOT a failure)
      ├─payment declined──────▶ incomplete → (retry) or expire → incomplete_expired
      └─session abandoned─────▶ incomplete_expired after TTL
```

Failure modes at creation:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------------------- |
| Checkout session expired | User abandoned | `incomplete_expired`; no entitlements |
| Payment method attach failed | Issuer/SDK error | Action-required code to client; keep session |
| First payment `requires_action` | SCA/3DS challenge | Store pending state; client resumes authentication |
| First payment declined | Issuer | Terminal for this attempt; show update-card flow |
| Webhook arrives before local row | Provider is faster than your commit | Insert-on-webhook via upsert keyed on provider ID |

**Key data:** Stripe `Subscription.status` values: `trialing`, `active`, `past_due`,
`canceled`, `incomplete`, `incomplete_expired`, `unpaid`, `paused`. PaymentIntent statuses:
`requires_payment_method`, `requires_confirmation`, `requires_action`, `processing`,
`succeeded`, `canceled`. Model *both* — the subscription status and the pending payment state —
or `requires_action` becomes indistinguishable from failure in your UI.

> ⚠️ **Hazard.** The browser redirect back from checkout is **not proof of payment**. Users
> close the tab, proxies cache the success page, and attackers replay the URL. The proof is
> the webhook or a server-side retrieve of the session by ID.

## 42.6 — Payment provider errors

Providers give you machine-readable codes. Treat them as a **classification table in your
registry**, never as message strings. Stripe's taxonomy (the most widely imitated) buckets
like this:

| Class | Example codes | HTTP | Retry? |
| ----- | ------------- | ---- | ------ |
| **Terminal, user-actionable** | `card_declined`, `expired_card`, `incorrect_cvc`, `insufficient_funds`, `incorrect_number` | 402 | ❌ Show message + update-card CTA |
| **Action-required (pending)** | `authentication_required` (SCA/3DS) | 402/200 w/ status | ❌ Not an error — resume auth flow |
| **Transient, retryable** | `rate_limit`, `processing_error`, provider `5xx`, connection errors | 429/5xx | ✅ Same idempotency key, backoff |
| **Request bugs** | `invalid_request_error`, `parameter_missing`, `resource_missing` | 400/404 | ❌ Fix the code |
| **Billing/account** | `insufficient_quota` (AI providers), account-level rate limit | 429 | ⚠️ Not until billing/config changes |

```ts
// The classification lives in one place — the error registry — not in catch blocks.
const PAYMENT_RETRY: Record<string, "retryable" | "action_required" | "terminal" | "bug"> = {
  card_declined: "terminal",
  expired_card: "terminal",
  incorrect_cvc: "terminal",
  insufficient_funds: "terminal",
  authentication_required: "action_required",
  rate_limit: "retryable",
  processing_error: "retryable",
  invalid_request_error: "bug",
};
```

**Key data:** Stripe rate-limits writes to **100 calls per 100 seconds per account** in live
mode (commonly **25** in test mode) and answers `429` with a `Retry-After` header. Never
hard-code RPM numbers from blog posts — **trust the response headers**, they are the contract.

## 42.7 — Duplicate payment attempts

Duplicates come from three directions, and each needs a different defense:

| Source | Defense |
| ------ | ------- |
| User double-click / impatient retry | Idempotency key generated **once per intent**, client-held, reused on retry |
| Client retries after network timeout | Same key — the provider collapses the attempts (see deep-dive) |
| Your worker re-processing a job | Deterministic key derived from the business operation, e.g. `charge:{orderId}` |

The rule: **an idempotency key identifies the business operation, not the HTTP request.** If
each retry generates a fresh key, you have built a duplicate-charge machine with good
observability.

```text
POST /api/checkout/payments
Idempotency-Key: ck_9f3b...            ← generated when the order was created
{ "orderId": "ord_123", "amount": 4900 }

attempt 1 → timeout (ambiguous!)        
attempt 2 → same key → provider replays the FIRST result (or 409 while in flight)
attempt 3 → same key, different amount → 400 idempotency_error (key misuse)
```

**Key data:** Stripe retains idempotency keys for **24 hours**. A retry with the same key and
the same parameters replays the stored response. A retry with the same key and **different**
parameters returns HTTP **400** with error type `idempotency_error`. A concurrent request with
the same key while the original is still in flight returns HTTP **409** (also
`idempotency_error`) — that is a "wait and re-read," not a failure.

## 42.8 — Ambiguous payment outcomes

After you send a charge and the connection dies, exactly one of these is true, and **you do not
know which**:

```text
              ┌─ request never reached provider  → safe to retry
send charge ──┼─ provider processed, response lost → retry = DOUBLE CHARGE (same key!)
              └─ provider received, still processing → retry too early = 409 or duplicate
```

This is the "unknown" state from the ambiguous-outcome model. The safe resolution order:

1. **Replay with the same idempotency key.** If the provider saw the first request, it returns
   the stored result — no duplicate. This is why keys are mandatory on money writes.
2. **Query the provider** (list charges / retrieve the PaymentIntent by your `metadata.orderId`)
   if the key is unavailable or older than the retention window.
3. **Park the order in `payment_pending_verification`** and let the reconciliation job (or
   webhook) settle it. Do not tell the user "failed."

**Never** "fail safe" by capturing again with a new key. The only safe default for an unknown
money outcome is *suspend and reconcile*.

## Worked example — Checkout double-click

Acme's `Checkout` button called `POST /payments` directly with a fresh key each press. During
a launch promo, 1.4% of sessions produced **two charges for one order**. Customers noticed
within hours; refunds and chargebacks followed. The fix, in order: (1) create the
PaymentIntent server-side when the checkout page loads and pin `Idempotency-Key` to the order
ID; (2) make the endpoint return the *same* result for the same key; (3) mark orders
`payment_pending_verification` on timeout and reconcile. Duplicate charges went to zero; the
remaining support volume was `requires_action` users who needed to complete 3DS — which the UI
now surfaces correctly instead of saying "payment failed."

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Key = HTTP request | Simple | Every retry is a new charge | Never for money |
| Key = business operation | Duplicate-safe | Key lifecycle must be managed | ✅ Default for payments |
| Provider-side keys only (24 h) | Zero local state | Blind beyond 24 h | Low volume, with reconciliation |
| Local key store + provider keys | Auditable, replayable | Extra table | High volume / financial SaaS |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every provider code once, in the registry | `catch (e) { retry(); }` on payment errors |
| Treat `authentication_required` as pending | Show it as "card declined" |
| Reuse the operation key on every retry | Mint a new key per attempt |
| On timeout: replay same key, then reconcile | Assume failure and re-capture |
| Trust `Retry-After` on 429 | Sleep a fixed 1 s |
| Mark unknown outcomes explicitly in your DB | Leave the order in a silent half-state |

## Common mistakes

- **Key per request** — retries become duplicates. Key per operation.
- **Retrying `card_declined`** — never succeeds; adds issuer risk flags.
- **Treating `requires_action` as failure** — SCA users are punished for strong auth.
- **Trusting the success redirect** — no webhook, no payment proof.
- **Re-capturing with a fresh key after a timeout** — the classic double charge.
- **Parsing error messages instead of codes** — provider wording changes; codes are the contract.

## Checklist

- [ ] Every money write requires an idempotency key derived from the business operation.
- [ ] Provider error codes map to retryable / action-required / terminal in one registry.
- [ ] Timeouts on payment writes produce an explicit `pending_verification` state.
- [ ] The client shows distinct UI for declined vs requires-action vs pending.
- [ ] Redirect success is never trusted without a webhook or server-side retrieve.
- [ ] 429 handling reads `Retry-After`.

## Related

- [Ambiguous Payment Outcomes and Idempotency](../02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md)
- [Checkout Subscription State Machine](../03-practical-examples/01-checkout-subscription-state-machine.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
