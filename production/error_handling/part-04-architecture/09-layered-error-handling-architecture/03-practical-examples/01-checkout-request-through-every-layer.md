# A `Checkout` Request Through Every Layer

> Part IV · Chapter 9 · All sections 9.1–9.20 · _Estimated reading time: 28 min_
> **Prerequisite:** [Where to Handle, Translate, and Propagate](../01-concepts/03-where-to-handle-translate-and-propagate.md)

## In one sentence

One `POST /checkouts` request, walked layer by layer, showing **exactly where each of five
realistic failures is detected, translated, handled, and rendered** — the end-to-end flow that
Chapter 9 promises.

## Why this matters in production

Diagrams don't stop leaks; a concrete trace does. When your team can point at a line and say
"here `23505` becomes `Conflict`, here the service decides, here the controller maps `409`,"
reviews get fast and incidents get short. This file is the template: copy the trace table, replace
the codes with yours.

## The request

```http
POST /api/v1/checkouts HTTP/1.1
Host: api.acme.example
Authorization: Bearer <tenant-token>
Idempotency-Key: 4f3a1c7e-8a44-4f2e-9d0b-3d5c1a2b9c11
Content-Type: application/json

{ "tenantId": "tnt_8412", "planId": "pro_annual", "paymentMethodId": "pm_1QxY..." }
```

## The layer path

```text
 PRESENTATION 9.1  (SPA submits form, renders field errors from the envelope)
 TRANSPORT    9.2  parse body · authn/authz · rate limit · payload size
 CONTROLLER   9.3  body → CreateCheckout command · outcome → status/body
 APPLICATION  9.4  transaction, orchestration, THE decision point
 DOMAIN       9.5  plan/seat invariants
 REPOSITORY   9.6  INSERT/SELECT on checkouts, tenants
 INFRASTRUCTURE 9.7  pool, config, cache
 INTEGRATION  9.8  Stripe (charge), email provider (receipt)
```

## Step-by-step with the five failure scenarios

**Step 1 — Transport (9.2) detects shape failures.** Nothing below runs.

```ts
// http/transport.ts
app.use(express.json({ limit: "256kb" }));          // oversized → 413 PAYLOAD_TOO_LARGE
app.use(bearerAuth);                                 // missing/invalid token → 401 UNAUTHORIZED
app.use(tenantGuard);                                // wrong tenant → 403 TENANT_FORBIDDEN
app.use(rateLimit({ key: (req) => req.tenantId }));  // over quota → 429 RATE_LIMITED + Retry-After
```

*Failure A — rate limit.* Detected and **handled at transport**: `429` +
`Retry-After: 30` + code `RATE_LIMITED`. The application service never runs. **Translation point
T5-adjacent:** transport-native statuses belong to the transport.

**Step 2 — Controller (9.3) maps input to a command.**

```ts
app.post("/api/v1/checkouts", async (req, res, next) => {
  try {
    const cmd = CreateCheckoutSchema.parse(req.body);   // Failure B: invalid body
    res.status(201).json(await createCheckout(cmd, req.auth, req.id));
  } catch (err) { next(toProblem(err, req.id)); }       // map-only; never retries
});
```

*Failure B — validation.* Detected in the controller's parse step, **rendered** as `422` with RFC
9457 `errors: [{ pointer: "/planId", code: "REQUIRED" }]`. No domain code involved.

**Step 3 — Application service (9.4) owns the transaction and the decision.**

```ts
export async function createCheckout(cmd: CreateCheckout, auth: Auth, corrId: string) {
  const tenant = await tenants.requireActive(cmd.tenantId, auth);   // may throw FORBIDDEN / NOT_FOUND
  const plan = await plans.get(cmd.planId);                          // may throw PLAN_NOT_FOUND
  return db.transaction(async (tx) => {
    const checkout = Checkout.start({ tenant, plan });               // DOMAIN errors originate here
    await checkoutsRepo(tx).insert(checkout);                        // may throw DUPLICATE_KEY
    const charge = await stripeCharges.charge(checkout, cmd.paymentMethodId); // INTEGRATION errors
    checkout.attachCharge(charge);
    await checkoutsRepo(tx).markActive(checkout);
    return checkout;
  });
}
```

**Step 4 — Domain (9.5) declares, never translates.**

```ts
// domain/checkout.ts — no imports beyond the domain
if (tenant.planSeatsUsed() >= tenant.seatLimit())
  throw new DomainError("SEAT_LIMIT_REACHED");          // Failure C
if (!plan.allowsTrial(tenant)) 
  throw new DomainError("TRIAL_NOT_ELIGIBLE");
```

*Failure C — seat limit.* **Originates in the domain**, propagates untouched through the
application (which has no handler for it), and is mapped by the controller to `409` with code
`SEAT_LIMIT_REACHED` and an upgrade hint. The domain never learns HTTP exists.

**Step 5 — Repository (9.6) translates persistence.**

```ts
// repo/checkout-repo.ts — translation point T1
try {
  await tx.none(SQL_INSERT, params);
} catch (err) {
  if (isSqlState(err, "23505")) throw { code: "DUPLICATE_KEY", key: "checkouts_tenant_plan", cause: err };
  if (isSqlState(err, "40001") || isSqlState(err, "40P01"))
    throw { code: "DB_UNAVAILABLE", retryable: true, cause: err };
  throw { code: "DB_UNAVAILABLE", retryable: true, cause: err };
}
```

*Failure D — duplicate checkout.* Postgres raises `SQLSTATE 23505`; **translated at the
repository**, **handled by the application service** (abort the transaction — no retry), **mapped
by the controller** to `409` + `CHECKOUT_ALREADY_EXISTS`. The raw `SQLSTATE` appears only in logs
via `cause`.

**Step 6 — Integration (9.8) normalizes Stripe.**

```ts
// integration/stripe.ts — translation point T2
export function normalizeStripe(e: Stripe.StripeError): AppError {
  if (e.type === "StripeCardError") return { code: "PAYMENT_CARD_DECLINED", declineCode: e.code ?? "unknown" };
  if (e.type === "StripeRateLimitError") return { code: "UPSTREAM_RATE_LIMITED", retryAfterSec: 2 };
  if (e.type === "StripeConnectionError") return { code: "UPSTREAM_UNAVAILABLE", retryable: true, cause: e };
  return { code: "UPSTREAM_ERROR", retryable: false, cause: e };
}
```

*Failure E — card decline.* Normalized to `PAYMENT_CARD_DECLINED`; the application service
**decides: no retry** (a decline is permanent — Part II classification), marks the checkout
`failed`, and the controller renders **`402`** + code + recovery hint (`402 Payment Required` is
the semantically right status for a failed charge). *Failure E′ — provider 429/timeout* is
classified retryable: the application performs **one** in-transaction retry honoring
`Retry-After`, then surfaces `503`.

**Step 7 — Presentation (9.1) renders the contract.**

The SPA reads only the RFC 9457 envelope: `type`, `title`, `status`, `detail`, `code`, `errors[]`,
`requestId`. Field errors attach to inputs; `5xx` classes render a retry affordance with the
`requestId` for support. It has no logic about *why* — the contract already said.

## The consolidated trace table

| # | Failure | Detected at (layer) | Translated at | Handled at | Rendered as |
| - | ------- | ------------------- | ------------- | ---------- | ----------- |
| A | rate limit | transport 9.2 | (native) | transport (reject) | `429` + `Retry-After`, `RATE_LIMITED` |
| B | invalid body | controller 9.3 | controller | controller (reject) | `422` + field `errors[]` |
| C | seat limit | domain 9.5 | — (already app vocabulary) | application (abort tx) | `409` `SEAT_LIMIT_REACHED` |
| D | duplicate key | infrastructure 9.7 | repository 9.6 (T1) | application (abort tx) | `409` `CHECKOUT_ALREADY_EXISTS` |
| E | card declined | integration 9.8 (T2) | integration | application (no retry, mark failed) | `402` `PAYMENT_CARD_DECLINED` |
| E′ | provider 429/timeout | integration 9.8 (T2) | integration | application (1 retry, then abort) | `429`/`503` + `Retry-After` |
| F | DB pool exhausted | infrastructure 9.7 | repository 9.6 | application (retry if idempotent) | `503` `DB_UNAVAILABLE` + `Retry-After` |
| G | anything unclassified | anywhere | nearest boundary | global handler (safety net) | `500` + `requestId`, no stack |

Read the table as Chapter 9's rules made visible: **every row has exactly one "handled at"**,
**translation happens at boundary layers only**, and **two entry points would produce the same
code** (9.19–9.20).

## Key data / numbers

- Statuses used above: `402`, `409`, `422`, `429`, `500`, `503` — plus transport-native `401`,
  `403`, `413`.
- `Retry-After` in seconds (HTTP-date or delta-seconds form); recommended client-visible values:
  `2–5` s for provider blips, `30` s for local rate limits.
- Idempotency: the `Idempotency-Key` header collapses duplicate `POST`s — one key, one recorded
  outcome, replayed on retry (Chapter 28).
- Postgres codes confined to T1: `23505`, `40001`, `40P01`.
- The whole happy path adds error-handling work at **6 translation points** and **1 decision
  point** — that is the budget for this endpoint.

## Real-world use case — Acme SaaS

Before this trace existed, Acme's `POST /checkouts` had three catch blocks in the controller,
retries in two layers, and Stripe errors passed through raw. Observed incident: a Stripe
degradation produced `500`s with Stripe object fragments in the body (disclosure risk) while
clients retried blindly, creating **duplicate pending subscriptions**. After the layering above:
declines became actionable `402`s, degradations became retryable `503` with `Retry-After`,
duplicate attempts collapsed via `Idempotency-Key`, and the Stripe fragment leak closed because
only the integration layer could see Stripe types.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Full trace per endpoint (this file) | Onboarding, review, and incident docs share one artifact | Costs an hour per critical endpoint | Your top 5–10 endpoints |
| Trace only on incidents | No upfront cost | Every incident re-derives the same map | Not recommended |
| No trace, conventions only | Zero cost | Conventions drift; new hires guess | Never for money paths |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every failure row exactly one "handled at" | Let transport or controller decide business outcomes |
| Keep domain rows translation-free | Add HTTP codes to domain errors |
| Record `cause` at T1/T2 for logs | Show raw driver/Stripe payloads to clients |
| Assert the trace table with integration tests | Treat the table as documentation-only |

## Common mistakes

- **A row with two handlers** — the most common is controller + application both retrying.
- **A row with no handler** — the error only reaches the global handler by accident; assign it.
- **Presentation logic creeping back in** — the SPA branching on message *strings* instead of
  `code` breaks the moment wording changes.

## Checklist

- [ ] Your critical endpoints have this trace table.
- [ ] Every row's "handled at" column names one layer.
- [ ] Transport-only failures never execute application code.
- [ ] The same fault injected via HTTP and via a job yields the same stable code.

## Related

- [Avoiding Duplicate Handling and Consistent Flow](../01-concepts/05-avoiding-duplicate-handling-and-consistent-flow.md)
- [Layer Contracts and Translation Points](../02-deep-dive/01-layer-contracts-and-translation-points.md)
- [Chapter 9 Reference — layer matrix](../05-reference/README.md)
- [Chapter 11 — The Error Lifecycle](../../11-the-error-lifecycle/README.md)
