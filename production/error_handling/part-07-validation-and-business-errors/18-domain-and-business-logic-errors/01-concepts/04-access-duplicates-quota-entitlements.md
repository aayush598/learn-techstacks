# Ownership, Duplicates, Quota, and Entitlements

> Part VII · Chapter 18 · Sections 18.5, 18.7–18.9 · _Estimated reading time: 22 min_
> **Prerequisite:** [What Domain Errors Are](./01-what-domain-errors-are.md)

## In one sentence

Four of the most frequent domain "no"s — **not yours**, **already exists**, **over quota/balance**,
**not in your plan** — each need a *named code, a deliberate status, and (where relevant) a
existence-hiding policy*, because they are also the four most security-sensitive answers your API
gives.

## Why this matters in production

These four families dominate real SaaS denial traffic, and each doubles as an information channel:
a careless `403` tells an attacker the resource exists; a careless `404` hides a bug report from a
legitimate customer; a `429` with no reset time makes clients hammer you; an entitlement error
without the plan name turns an upsell moment into a support ticket. Precision here is product,
security, and operability at once.

## 18.5 — Ownership and access

```text
 authenticated ──▶ owns it? ──▶ yes → continue
                        │
                        no ──▶ policy: 404 (hide)  or  403 (admit + explain)
```

| Policy | Response | Use when | Trade-off |
| ------ | -------- | -------- | --------- |
| **Hide existence** | `404 NOT_FOUND` (same body as real miss) | Multi-tenant data users could probe | Slightly worse UX for legit users with stale links |
| **Admit + forbid** | `403 NOT_OWNER` / `INSUFFICIENT_ROLE` | Internal tools, trusted tenants | Confirms existence to probers |
| **Admit, redact** | `403` with no ownership details | Middle ground | — |

Consistency requirements either way:

- **Same shape as a true miss** if hiding (identical status *and* body *and* timing posture —
  see Ch. 34/35 for timing side channels).
- **Authn vs authz split:** no credentials → `401`; credentials but no rights → `403` (or the
  chosen `404`). Never `401` for a rights problem (the client would just re-auth forever).
- Codes: `NOT_OWNER`, `INSUFFICIENT_ROLE`, `TENANT_MISMATCH` (internal; usually rendered as the
  public `403`/`404` above).

## 18.7 — Duplicate and uniqueness

Uniqueness is a **domain rule with a persistence backstop**:

```text
 service pre-check (fast path, UX)  ──▶  INSERT  ──▶  unique index (source of truth)
        │                                                  │
        └── "probably taken" → 409                          └── 23505 → translate → 409
            (still must handle the race)                       (never leak the index)
```

Key rules:

- **The unique index is the truth; the pre-check is an optimization.** A `23505` that arrives
  without a prior pre-check is not an error condition — it is the race you always expected:
  translate to the **same** `409 ALREADY_EXISTS` code ([Ch. 16 map](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)).
- **One code, field detail:** `ALREADY_EXISTS` + `details.field = "email"` — never
  `EMAIL_ALREADY_TAKEN` + `SLUG_ALREADY_TAKEN` + … as separate codes (rule-level codes; 17.14
  logic applies to the domain registry too).
- **Idempotent creates collapse to success:** with an idempotency key or natural-key
  semantics, "already exists with the same content" may be a `200` replay; "same key, different
  payload" is `409` + explanation ([Ch. 28](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)).
- **Cross-tenant uniqueness** must be scoped in the index (`(tenant_id, email)`) or you will
  either leak existence across tenants or reject valid signups.

```json
{
  "code": "ALREADY_EXISTS",
  "category": "CONFLICT",
  "details": { "field": "email", "resource": "invitation" },
  "httpStatus": 409
}
```

## 18.8 — Insufficient balance and quota

Two different resource denials that clients experience differently:

| Kind | Meaning | Status (recommended) | Extra guidance |
| ---- | ------- | -------------------- | -------------- |
| **Balance** (money/credit) | Account cannot pay | `402 Payment Required` | `details.due`, payment method link |
| **Quota** (seats, storage, jobs) | Count/limit reached | `409` (conflict with limit) or `429` (rate family) — **pick one policy** | `details.limit`, `details.current`, `details.resetAt` |
| **Rate** (requests/min) | Temporal throttle | `429` + `Retry-After` | Ch. 19/27 |

⚠️ **Hazard.** Do not squash balance into `429` or quota into `402`: clients use `429` for
automatic backoff, and a backed-off *payment* retry is a bug, not a resilience feature. Money
denials need a human in the loop (`402`), rate denials need a timer (`429`).

```json
{
  "code": "SEAT_QUOTA_EXCEEDED",
  "category": "QUOTA",
  "details": { "requested": 30, "current": 12, "limit": 12, "plan": "pro",
               "resetAt": null, "upgradeRequired": true },
  "httpStatus": 402
}
```

`upgradeRequired` and `plan` turn the denial into an **upsell surface** — the client can offer
the exact next step instead of a dead end. (Quota *rate* limits stay in the 429 family with
`Retry-After`; persistent capacity limits are not rates and should not borrow that machinery.)

## 18.9 — Subscription and entitlement

Entitlement asks: **"does this account's plan/flags grant capability X right now?"** — evaluated
by an **entitlement resolution** step (plan features + add-ons + overrides + trial flags):

```ts
export function requireEntitlement(tenant: Tenant, cap: Capability): Result<void, DomainError> {
  const ent = entitlements.resolve(tenant);     // plan + addons + overrides + trial
  if (!ent.grants(cap)) {
    return err(new EntitlementMissing(cap, {
      plan: ent.planCode,
      entitledPlans: plans.granting(cap),        // "business", "enterprise"
      effectiveUntil: ent.effectiveUntil ?? null,
    }));
  }
  return ok(undefined);
}
```

Rules of a good entitlement error:

- **Name the capability** (`"sso"`, `"audit_log"`), not the product marketing tier only.
- **`entitledPlans`** gives the client a concrete upgrade path (a ranked list, cheapest first).
- **Trial expiry is an entitlement transition**, not a mysterious 403 six weeks later: when the
  trial ends, the same `ENTITLEMENT_MISSING` now carries `reason: "trial_expired"` +
  `effectiveUntil` in the past.
- Status: **`403`** (authenticated, not allowed) with the code doing the explaining — or `402`
  when the remedy is strictly payment; keep the choice consistent per capability family.
- Suspension for non-payment is a **lifecycle transition** (18.6) that *causes* entitlement
  loss — model the transition and the entitlement separately so both explanations exist.

## Key data / numbers

- Ownership: `401` no creds · `403` no rights · `404` hide-existence policy — never mix.
- Duplicates: `409 ALREADY_EXISTS` + `details.field`; DB origin `SQLSTATE 23505`.
- Balance: `402`; quota-capacity: `409` (recommended) with `limit`/`current`; rate: `429` +
  `Retry-After`.
- Entitlement: `403` + `capability`, `plan`, `entitledPlans`; trial expiry = same code +
  `reason: "trial_expired"`.
- All four are **permanent for an identical request** (no retry) unless the caller changes
  account, plan, or capacity.

## Real-world use case — Checkout + WebhookIngest

Acme's self-serve upgrade flow returned `403 Forbidden` for: another workspace's project (probe-
able existence leak), seat quota, SSO entitlement missing, and unpaid balance. Clients could not
branch; one integration auto-retried the 403s for an hour. The four became `404` (cross-tenant,
identical body to true miss), `402 SEAT_QUOTA_EXCEEDED` with `limit`/`current`, `403
ENTITLEMENT_MISSING` with `entitledPlans`, and `402 PAYMENT_METHOD_REQUIRED`. Separately,
`WebhookIngest` had treated `invoice.payment_failed` as infrastructure and retried it through the
queue; it is a *domain event* — the correct handling is a lifecycle transition to `past_due` plus
a customer-visible `402` on the next action, not queue retries. Retried webhooks stopped; dunning
started working as designed.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Hide existence (`404`) | Anti-enumeration | Confusing for legitimate stale links | Multi-tenant user data ✅ |
| Admit + `403` | Clear UX, actionable | Existence oracle | Trusted/internal, public resources |
| Pre-check + DB backstop for uniqueness | Fast path + correctness | Must handle both paths identically | ✅ Always |
| Upsell-rich quota errors | Revenue surface | Slightly larger payload | ✅ Consumer/self-serve flows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pick one existence-hiding policy and apply it per resource family | Mix `403` and `404` for the same resource class |
| Translate `23505` to the same code as the pre-check | Leak constraint/index names |
| Separate `402` (money), `409` (capacity), `429` (rate) | Auto-retry `402`/`409` like a `429` |
| Name capabilities and list `entitledPlans` | Return anonymous "forbidden" |

## Common mistakes

- **`403` on cross-tenant access** — confirms the id exists; use the hide policy.
- **Quota error without numbers** — client cannot say how many seats to buy.
- **Treating entitlement as authentication** — users re-login instead of upgrading.
- **Dunning via webhook retries** — a failed payment is domain state, not a transient job.

## Checklist

- [ ] Existence-hiding policy documented per resource family; consistent bodies.
- [ ] `401`/`403`/`404` used with their exact meanings; no "forbidden" catch-all.
- [ ] Uniqueness: DB index is truth; both paths yield one code; race handled.
- [ ] Balance/quota/rate have three distinct codes and statuses.
- [ ] Entitlement errors name the capability and the entitled plans.
- [ ] Trial expiry and suspension surface as explicit reasons, not mystery 403s.

## Related

- [State Transitions and Lifecycle](./03-state-transitions-and-lifecycle.md)
- [Entitlement, Lifecycle, and Webhook Examples](../03-practical-examples/02-entitlement-lifecycle-and-webhooks.md)
- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 42 — Auth, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
