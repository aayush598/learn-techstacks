# Entitlement Denials, Illegal Transitions, and Duplicate Webhooks

> Part VII · Chapter 18 · All sections · _Estimated reading time: 22 min_
> **Prerequisite:** [Value Objects and Domain Errors](./01-value-object-money-and-domain-errors.md)

## In one sentence

Three end-to-end scenarios from the recurring cast: an **entitlement denial** that doubles as an
upsell (`Checkout`), an **illegal lifecycle transition** with an `allowed` map (`ExportJob`), and
**duplicate/out-of-order webhooks** that must collapse into idempotent domain outcomes
(`WebhookIngest`).

## Why this matters in production

These three scenarios cover the majority of "the business says no" traffic in a billing-heavy
SaaS — and each has a signature failure mode: entitlement denials that look like outages, illegal
transitions that corrupt state machines, and webhook replays that double-charge. All three are
*expected domain behavior*; all three become outages only when modeled as generic errors.

## Scenario 1 — Entitlement denial (`Checkout`)

Tenant on `pro` attempts to enable SSO mid-session.

```ts
// application service:
const outcome = changePlanWithCapability(tenant, { capability: "sso" }, ctx);
// → err(EntitlementMissing) → transport:
```

```json
{
  "type": "https://errors.acme.example/forbidden",
  "title": "ENTITLEMENT_MISSING",
  "status": 403,
  "detail": "The pro plan does not include sso.",
  "requestId": "req_77aa10",
  "capability": "sso",
  "plan": "pro",
  "entitledPlans": ["business", "enterprise"],
  "reason": "plan_limit"
}
```

Client contract (documented for the SDK):

| Field | Client use |
| ----- | ----------|
| `capability` | Which upsell card to render |
| `entitledPlans` | Ordered upgrade options (cheapest first) |
| `reason` | `plan_limit` vs `trial_expired` vs `suspended` — different copy, same code |
| `status 403` | **Not** a retry; not an auth loop |

`reason` values are part of the contract — adding one is additive; renaming one is breaking
(18.20). Suspension-for-non-payment surfaces as `reason: "suspended"` from the *lifecycle*
transition (18.6), not a second code — one code, richer reasons.

## Scenario 2 — Illegal transition (`ExportJob`)

Client cancels a job that is already `finalizing` (near-complete; aborting would discard the
object):

```json
{
  "type": "https://errors.acme.example/conflict",
  "title": "INVALID_TRANSITION",
  "status": 409,
  "detail": "The job cannot be canceled while finalizing.",
  "requestId": "req_c31f02",
  "action": "cancel",
  "state": "finalizing",
  "allowed": [],
  "stateReason": "finalizing_near_complete",
  "blocking": { "kind": "export_job", "id": "job_71a2" }
}
```

Why each member earns its place:

- **`allowed: []`** — the client stops showing a cancel button instead of guessing which arrows
  exist.
- **`stateReason`** — the difference between "cancel rejected, try later" and "cancel rejected,
  it would discard 40 minutes of work" is a support call if omitted.
- **`409` + no `Retry-After`** — retrying the identical cancel cannot succeed; the remedy is a
  refresh, not a timer. Contrast with `OPERATION_IN_PROGRESS`, which *does* carry `retryAfterMs`.

```ts
// transition table excerpt — cancel legal only from these states
cancel: { queued: "canceling", running: "canceling", paused: "canceling" },
// finalizing/canceled/completed/failed → INVALID_TRANSITION (idempotent cancel on
// canceled → success no-op, per the action's idempotency contract)
```

## Scenario 3 — Duplicate and replayed webhooks (`WebhookIngest`)

The provider retries deliveries (at-least-once; Ch. 33). Each event must produce **one** domain
effect:

```text
 POST invoice.payment_failed #evt_1 ──▶ verify sig ──▶ dedupe store (event id)
                                          │                    │
                                          ├─ first time  ─────▶ apply transition:
                                          │                    active→past_due (emit fact)
                                          └─ duplicate   ─────▶ 200 OK, no effect
 POST invoice.payment_failed #evt_1 ──▶ 200 OK (replay, identical)
 POST invoice.payment_failed #evt_2 (newer) ──▶ 200 OK, effect applied once
```

```ts
async function handle(evt: StripeEvent) {
  if (await seen.has(evt.id)) return ok200("duplicate");        // collapse, not an error
  const result = await applyBillingEvent(evt);                  // domain decides transition
  if (result.isErr) {
    // Domain denial on a webhook: log + 400 (provider will not fix it) — NEVER a 5xx
    // retry loop, and never a 2xx that pretends the effect happened.
    log.warn({ code: result.error.code, eventId: evt.id }, "webhook domain denial");
    return respond(400);
  }
  await seen.mark(evt.id, { code: result.ok?.code ?? "applied" });
  return ok200("applied");
}
```

Decision table for webhook outcomes:

| Situation | HTTP | Domain effect | Note |
| --------- | ---- | ------------- | ---- |
| Signature invalid | `400` | none | No detail pre-auth (17.17) |
| Unparseable | `400` | none | |
| Duplicate event id | `200` | none | **Not an error** — the desired outcome |
| Valid, transition applied | `200` | one | `active → past_due` etc. |
| Valid, transition illegal | `400` | none | e.g. cancel on `canceled` — log code; provider retry won't help |
| Valid, infra failure (DB down) | `5xx` | none | Retry is correct here — transient (Ch. 27) |

The subtle one: **an illegal transition from a replayed event is not a `500`.** The event
arrived too late (out-of-order; Ch. 33) — that is a domain-time conflict: acknowledge with a
non-retryable status and log, or store it for reconciliation, but never let the provider hammer a
`500` for an outcome that can never change.

## Key data / numbers

- Entitlement: `403` + `capability`, `plan`, `entitledPlans[]`, `reason`
  (`plan_limit`|`trial_expired`|`suspended`).
- Transition: `409` + `action`, `state`, `allowed[]`, `stateReason`; `Retry-After` **only** when
  waiting genuinely helps.
- Webhook dedupe: key = provider event id, TTL ≥ provider retry window (Stripe: commonly up to
  ~3 days — verify your provider's documented window and exceed it).
- Duplicate webhook → **`200` + no effect**, indistinguishable from a fresh success.

## Real-world use case — Checkout + WebhookIngest at Acme

During a dunning rollout, `invoice.payment_failed` was processed twice for the same event (retry
after a transient 500 *after* the state had already changed): the subscription flipped
`active → past_due → suspended` in 90 seconds, enterprise support pages lit up, and customers
could not access projects. The fix combined all three scenarios' lessons: event-id dedupe
*before* domain application, transitions modeled as a table (`active→past_due` legal;
`past_due→suspended` legal; `suspended→suspended` idempotent no-op), and illegal/replayed
transitions acknowledged with `200`/`400` + structured logs instead of `5xx`. Dunning then
processed 1.4M events/month with zero double-suspensions.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Rich `details` on denials | Upsell/guidance surface; fewer tickets | Larger payloads; contract surface | ✅ Consumer flows |
| Bare `403`/`409` | Minimal | Dead-end UX; support load | Internal tools |
| Dedupe-before-domain | Exactly-once effect | Store + TTL to operate | ✅ Webhooks |
| Idempotent transition no-ops | Replay-safe | Requires per-action idempotency decision | ✅ State machines |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Include `entitledPlans` on entitlement denials | Return anonymous "forbidden" |
| Ship `allowed` + `stateReason` with transition errors | Bare "invalid operation" |
| Collapse duplicate events to `200` + no-op | Treat replays as errors or re-apply effects |
| Acknowledge late/out-of-order events non-retriably | `500` a provider into an infinite retry |

## Common mistakes

- **Dedupe after domain application** — the exact window the double-suspension exploited.
- **`allowed` hardcoded in the client** — adding a state breaks every app version.
- **Using `reason` for branching while renaming it casually** — it is contract (18.20).
- **Returning `5xx` for domain denials on webhooks** — infinite provider retries against a
  permanent outcome.

## Checklist

- [ ] Entitlement denials carry capability + plan + entitledPlans + reason.
- [ ] Transition errors carry action + state + allowed + stateReason.
- [ ] Action idempotency decided (no-op vs `409`) and tested.
- [ ] Webhook dedupe keyed on event id, applied before domain logic, TTL > retry window.
- [ ] Webhook status policy table implemented exactly (no `5xx` for domain denials).

## Related

- [Value Objects and Domain Error Examples](./01-value-object-money-and-domain-errors.md)
- [State Transitions and Lifecycle](../01-concepts/03-state-transitions-and-lifecycle.md)
- [Ownership, Duplicates, Quota, and Entitlements](../01-concepts/04-access-duplicates-quota-entitlements.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
