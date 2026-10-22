# Decision Walkthrough: The `Checkout` Flow

> Part XXII · Chapter 56 · Sections 56.1–56.18 (applied) · _Estimated reading time: 25 min_
> **Prerequisite:** [Chapter 56 README](../README.md), [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)

## In one sentence

A single, complete walk through the `Checkout` flow showing **how the 18 pairs are decided in
practice**, what the code looks like before and after, and how to record the decisions so the
next engineer does not reopen them.

## Why this matters in production

`Checkout` is where every competing approach meets: a database write, an external payment
provider, an entitlement change, an email, and money. It is the flow most likely to be
reviewed under pressure and the one where a wrong decision is most expensive.

The value of a walkthrough is not the answer — it is the **reasoning order**. When a new
engineer asks "should this be a `Result` or a thrown error?", the answer is not a style
preference; it is derived from four inputs:

1. The **failure set** of the operation (enumerable or not).
2. The **caller** (who needs to branch, and on what).
3. The **risk tier** (what breaks if we are wrong).
4. The **boundary** (who owns the fallback).

## The starting point

Here is Acme's `Checkout` as it existed, condensed but faithful:

```ts
// ❌ BEFORE — one file, five decisions never made.
app.post("/checkout", async (req, res) => {
  try {
    const { planId, seats } = req.body;
    const plan = await db.query(`SELECT * FROM plans WHERE id=$1`, [planId]);   // may throw
    if (!plan.rows[0]) throw new Error("plan not found");                        // generic

    await db.query(`UPDATE plans SET seats = seats - $1 WHERE id = $2`, [seats, planId]);

    const charge = await stripe.charges.create({                                // may throw
      amount: plan.rows[0].price * seats,
      currency: "usd",
      source: req.body.token,
    });

    await db.query(`INSERT INTO subscriptions (...) VALUES (...)`);              // may throw
    await sendEmail(req.body.email, "Welcome!");                                // may throw

    res.status(201).json({ subscriptionId: 1 });
  } catch (err) {
    log.error(err);
    res.status(500).json({ error: "Something went wrong" });                    // everything is 500
  }
});
```

Nine distinct defects are visible in 22 lines. Each one is a decision the team never made.
The table below maps each to the pair it belongs to.

| # | Defect | Subsection |
| - | ------ | ----------- |
| 1 | "plan not found" is a generic `Error` | 56.9 generic vs specific |
| 2 | `plan.rows[0]` may be undefined → `TypeError` on `.price` | 56.1 exceptions vs results |
| 3 | Seat decrement is not rolled back if Stripe fails | 56.6 retry vs compensation |
| 4 | Stripe charge is retried by *the client* with no idempotency key | 56.5 / 56.6 |
| 5 | No idempotency key on the charge | 56.5 retry eligibility |
| 6 | Subscription insert failure leaves a charged customer | 56.6 |
| 7 | Email failure aborts the whole checkout | 56.4 fail-fast vs degradation |
| 8 | Every error becomes a `500` | 56.2 centralized vs local, 56.18 tiering |
| 9 | `log.error(err)` with no correlation ID | 56.8 preserving |

## The decisions, one by one

### Decision 1 — control-flow shape (56.1, 56.7, 56.14)

**Question asked:** *Can the caller enumerate the failure set of `startCheckout`?*

**Answer:** Yes, almost. The failures are: plan not found, plan not purchasable, seats
unavailable, card declined, insufficient funds, provider unavailable, provider rate-limited,
activation failed. That is **8 variants** — close to the ceiling for a union, and clearly
enumerable.

**Decision:** the domain returns a `Result`; the adapter throws vendor errors until they are
translated; the transport catches once.

```ts
export type CheckoutError =
  | { code: "PLAN_NOT_FOUND" }
  | { code: "PLAN_NOT_PURCHASABLE" }
  | { code: "SEATS_UNAVAILABLE" }
  | { code: "PAYMENT_CARD_DECLINED"; declineCode: string }
  | { code: "PAYMENT_INSUFFICIENT_FUNDS" }
  | { code: "PAYMENT_PROVIDER_RATE_LIMITED"; retryAfterSeconds: number }
  | { code: "PAYMENT_PROVIDER_UNAVAILABLE" }
  | { code: "SUBSCRIPTION_ACTIVATION_FAILED" };

export type CheckoutOutcome =
  | { ok: true; subscriptionId: string }
  | { ok: false; error: CheckoutError };
```

The 8 variants exceed the "3–7" guideline by one, which is the signal to split the union
into *known* and *unknown* — which is exactly what the final `catch` produces:

```ts
| { code: "UNKNOWN"; cause: unknown }   // always present, always permanent
```

### Decision 2 — where the fallback lives (56.2)

**Question asked:** *Who owns the fallback — the global handler or the route?*

**Answer:** the **route**, because the fallback differs per surface. The API returns a
problem document; a CLI would print a different message; a background job would record a
different failure shape. What is shared is the *registry* (code → status, title, retryable),
not the fallback.

### Decision 3 — error class shape (56.3, 56.9, 56.10)

**Answer:** one `CheckoutError` class with a discriminated `code` — not eight subclasses and
not a generic `IntegrationError`. The `code` union makes the caller able to branch exhaustively
with `assertNever`, which is the compiler benefit of composition over inheritance.

### Decision 4 — risk tiers (56.18)

| Operation | Tier |
| --------- | ---- |
| Validate the request | T2 |
| Reserve seats | T2 |
| Charge the card | **T3** |
| Activate the subscription | **T3** |
| Send the welcome email | T1 |
| Write the audit entry | **T4** |

### Decision 5 — fail fast vs degrade (56.4)

- **Degrade**: the welcome email (T1). A missing email is a nuisance; blocking a purchase on
  it is absurd.
- **Fail fast**: seats (T2 — a checkout without a seat is wrong), charge (T3), activation
  (T3), audit (T4).

### Decision 6 — retry vs immediate failure (56.5)

Retry only `PAYMENT_PROVIDER_UNAVAILABLE` and `PAYMENT_PROVIDER_RATE_LIMITED`, only with an
`Idempotency-Key`, only while the deadline allows (3 attempts, exponential backoff with full
jitter, honoring `Retry-After` up to 60 s). `PLAN_NOT_FOUND`, `SEATS_UNAVAILABLE`, and card
declines get **0** attempts.

### Decision 7 — retry vs compensation (56.6)

The critical question is "has the effect happened?":

```text
  seat reserved?  no  → retry the reservation (idempotent by reservation key)
                yes  → continue
  card charged?   no  → release the seat; fail with the provider error
                yes  → continue
  subscription
  activated?     no  → refund the charge (idempotency key `refund:{chargeId}`),
                       release the seat, fail
                yes  → continue
```

### Decision 8 — wrapping vs preserving (56.8)

The Stripe error is wrapped into `CheckoutError` with `cause`, `vendorCode`
(`card_declined`), and `vendorRequestId` (`req_9f2…`). Nothing is parsed from a message.

### Decision 9 — sync vs deferred (56.15)

The whole checkout is **synchronous**: the user is on the page. The *email* is deferred (an
outbox row written in the same transaction, sent by a worker later). That is 56.15 applied at
the right granularity — not "the whole flow is sync" but "the part the user waits for is sync".

### Decision 10 — local recovery vs termination (56.16)

Every failure here is recovered locally. Termination is reserved for T4 audit failures, where
Acme quarantines the request rather than continuing.

## The result

```ts
// ✅ AFTER — the decisions are visible in the shape of the code.
export type CheckoutError =
  | { code: "PLAN_NOT_FOUND" }
  | { code: "PLAN_NOT_PURCHASABLE" }
  | { code: "SEATS_UNAVAILABLE" }
  | { code: "PAYMENT_CARD_DECLINED"; declineCode: string }
  | { code: "PAYMENT_INSUFFICIENT_FUNDS" }
  | { code: "PAYMENT_PROVIDER_RATE_LIMITED"; retryAfterSeconds: number }
  | { code: "PAYMENT_PROVIDER_UNAVAILABLE" }
  | { code: "SUBSCRIPTION_ACTIVATION_FAILED" }
  | { code: "UNKNOWN"; cause: unknown };

export type CheckoutOutcome =
  | { ok: true; subscriptionId: string }
  | { ok: false; error: CheckoutError };

export async function startCheckout(
  input: CheckoutInput,
  ctx: { correlationId: string; idempotencyKey: string },
): Promise<CheckoutOutcome> {
  const plan = await plans.findPurchasable(input.planId);
  if (!plan.ok) return { ok: false, error: plan.error };

  const seat = await seats.reserve(input.tenantId, input.planId, input.seats, {
    idempotencyKey: `${ctx.idempotencyKey}:seat`,
  });
  if (!seat.ok) return { ok: false, error: seat.error };

  // T3 write: an idempotency key is mandatory before any retry is possible.
  const charge = await payments.charge(
    { amountMinor: plan.value.priceMinor * input.seats, currency: "usd", token: input.token },
    { idempotencyKey: `${ctx.idempotencyKey}:charge`, timeoutMs: 5_000 },
  );
  if (!charge.ok) {
    await seats.release(seat.value.reservationId);        // compensate step 1
    return { ok: false, error: charge.error };
  }

  const activation = await subscriptions.activate(charge.value.chargeId, {
    idempotencyKey: `${ctx.idempotencyKey}:activate`,
  });
  if (!activation.ok) {
    await payments.refund(charge.value.chargeId, {
      idempotencyKey: `refund:${charge.value.chargeId}`,    // compensation is idempotent
    });
    await seats.release(seat.value.reservationId);
    return { ok: false, error: activation.error };
  }

  await outbox.enqueue("welcome_email", { subscriptionId: activation.value.subscriptionId });
  return { ok: true, subscriptionId: activation.value.subscriptionId };
}
```

The transport is the only place that knows HTTP:

```ts
app.post("/checkout", async (req, res) => {
  const parsed = parseCheckoutRequest(req.body);          // strict → 422 with field errors
  if (!parsed.ok) return res.status(422).json(problemFromFields(parsed.error, req.id));

  const outcome = await startCheckout(parsed.value, {
    correlationId: req.id,
    idempotencyKey: req.header("Idempotency-Key") ?? req.id,
  });

  if (outcome.ok) return res.status(201).json({ subscriptionId: outcome.subscriptionId });

  const meta = registry.get(outcome.error.code);           // centralized policy
  if (meta.retryable) res.setHeader("Retry-After", String(meta.retryAfterSeconds ?? 5));
  res.status(meta.httpStatus).json(problemFrom(outcome.error, req.id, meta.publicTitle));
});
```

## The decision record

The decisions above were captured in an ADR so that a future engineer does not reopen them.
The template matters more than the content:

```text
# ADR-014 — Checkout error-handling approach

Status: accepted · Date: 2026-04-18 · Owners: @acme/payments

Context
  The checkout flow mixed exceptions, null returns, and generic errors. 41% of checkout
  failures returned 500; support handled ~18 "charged but no access" tickets/month.

Decisions (one line each, with the subsection it came from)
  1. Domain returns a closed Result union.                 (56.1, 56.7)
  2. Adapters translate vendor errors and preserve cause.   (56.8)
  3. Registry owns status/retryable/title. Route owns fallback. (56.2)
  4. One CheckoutError class, discriminated code union.      (56.3, 56.9, 56.10)
  5. Charge + activation are T3; email is T1; audit is T4.  (56.18)
  6. Retry only with an idempotency key, max 3, jittered.   (56.5)
  7. Compensation on completed T3 effects, reverse order.   (56.6)
  8. Email deferred via outbox; checkout itself synchronous. (56.15)

Consequences
  + Checkout 5xx rate dropped from 41% of failures to 4%.
  + "Charged but no access" tickets: 18/month → 0.
  + Every new failure reason needs 1 registry entry, no controller edit.
  − The union grew to 9 variants; a split may be needed if it exceeds ~12.

Revisit when
  - The union exceeds 12 variants.
  - A second payment provider is added (the adapter boundary should absorb it).
```

## Key data / numbers

| Metric | Before | After | Note |
| ------ | ------ | ----- | ---- |
| Checkout failures returned as `500` | 41% | 4% | Remaining 500s are T4/unknown |
| "Charged but no access" tickets | 18/month | 0 | Compensation + idempotency |
| Registry entries needed for a new decline reason | 3 files | 1 file | Registry + adapter |
| Retry attempts on the provider call | unbounded (client-driven) | 3, idempotency-keyed | With jitter |
| `Retry-After` emitted on a retryable `5xx` | never | 5 s | Honored up to 60 s |
| Validation response | `500` on a bad body | `422` + field list | ≤ 20 field errors |
| Compensation window | n/a | 24 h | Beyond → manual review |
| Idempotency key TTL | 24 h | 24 h | Matches the provider's de-duplication window |

## Real-world use case — the "charged but no access" incident

Acme's checkout created a Stripe charge, then failed to write the subscription row because of
a transient Postgres serialization failure (`SQLSTATE 40001`). The original code did not
retry and did not compensate, so the customer was charged and had no entitlement. 18
customers hit this in one month; 6 of them filed chargebacks.

The postmortem identified the missing decisions, not a missing `try/catch`:

1. **No tier** → nobody had decided that a charge is T3 and a subscription insert is T3, so
   nobody thought to compensate.
2. **No idempotency** → the obvious fix (retry the insert) would have been safe, but nobody
   realized the *charge* was also at risk if the flow were retried from the top.
3. **No compensation** → the refund path did not exist, so the failure had nowhere to go
   except to a human.

The fix was the decision record above. The measurable result: **chargebacks from checkout
failures dropped from 6/month to 0**, and the checkout's 5xx rate fell from 41% of failures to
4% — with the remaining 4% being genuine unknown failures, which now alert instead of
silently becoming a customer complaint.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One `catch` at the route | Small diff | Hides every decision; wrong policies | Legacy code being stabilized |
| Domain `Result` + registry + tiers | Every decision explicit and reviewable | More types; more ceremony up front | Payment, entitlement, anything with money |
| Exception-only with a rich class | Familiar | Caller cannot branch reliably | Internal-only services |
| Per-step try/catch | Local recovery | Easy to double-handle and drift | Only where a fallback differs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide the shape from the failure set and the caller | Decide it from language taste |
| Write the tier for each operation in the flow | Apply one policy to the whole flow |
| Compensate a completed T3 effect before returning | Return an error and leave the charge behind |
| Use an idempotency key on every T3 write | Retry the flow from the top after a partial failure |
| Capture the decision in an ADR | Let the next engineer reverse-engineer it |

## Checklist

- [ ] Every failure of the flow has a named code in the domain union.
- [ ] Every operation in the flow has a tier.
- [ ] Retry, degrade, compensate, and terminate decisions exist per code.
- [ ] T3 writes carry an idempotency key.
- [ ] Compensations are ordered and idempotent.
- [ ] The transport is the only layer that knows HTTP status codes.
- [ ] An ADR records the decisions and when to revisit them.

## Related

- [ExportJob and AgentRun: The Same Matrix, Different Answers](./02-exportjob-and-agentrun-selection-matrix.md)
- [Risk-Based Policy Selection](../02-deep-dive/02-risk-based-policy-selection.md)
- [Recovery Policy Trade-offs](../01-concepts/03-recovery-policy-tradeoffs.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
