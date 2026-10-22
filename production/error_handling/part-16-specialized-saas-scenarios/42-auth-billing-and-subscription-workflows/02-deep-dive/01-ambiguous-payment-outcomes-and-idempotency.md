# Ambiguous Payment Outcomes and Idempotency — Mechanics

> Part XVI · Chapter 42 · Sections 42.7, 42.8, 42.16 · _Estimated reading time: 24 min_
> **Prerequisite:** [Subscription and Payment Errors](../01-concepts/02-subscription-and-payment-errors.md)

## In one sentence

A network call to a payment provider has **three** outcomes — success, definite failure, and
**ambiguous** — and safe financial operations require that every ambiguous outcome be
resolvable by **idempotent replay or provider lookup**, never by guessing.

## Why this matters in production

Non-financial code usually models a call as success-or-throw. That model is *wrong* exactly
where it costs the most: after a timeout on `POST /charges`, the charge may exist. Code that
throws-and-retries creates a second charge; code that catches-and-ignores loses the first one.
The ambiguous state is not an edge case to handle with a bigger try/catch — it is a **state
your data model must represent** and a **workflow your workers must execute**.

## The three-way outcome model

```text
                    send(charge)
                         │
        ┌────────────────┼─────────────────────┐
        ▼                ▼                     ▼
   HTTP 2xx          HTTP 4xx/5xx        no / broken response
   success           DEFINITE failure    AMBIGUOUS
   (charge exists)   (charge did not     (unknown: request lost,
                     happen — for        half-sent, response lost,
                     terminal codes)     or still processing)
```

- **Definite failure** covers `card_declined` (the provider evaluated and refused) and
  *request-shape* failures (`invalid_request_error`) — no money moved.
- **Ambiguous** covers: connect timeout (maybe never arrived), read timeout after send
  (arrived, response lost), `502`/`504` from the provider's own gateway (unknown), and
  connection reset mid-response. In all four, **the charge may exist**.
- The provider's own `processing` status is a *declared* ambiguity — the provider is telling
  you the outcome is pending; poll or wait for the webhook.

The rule that follows: **ambiguous is never "retry with a fresh key."** It is
"replay with the same key" or "look it up."

## Idempotency-key mechanics (Stripe model)

How provider-side keys actually behave — these numbers are the contract you design against:

| Event | Provider behavior |
| ----- | ----------------- |
| First request with key K | Executes; stores response for **24 hours** |
| Retry, same K, same params | **Replays stored response**; no second charge |
| Retry, same K, different params | HTTP **400**, type `idempotency_error` — key misuse |
| Retry, same K, original still in flight | HTTP **409**, type `idempotency_error` — wait and re-read |
| Key older than 24 h, retried | Treated as a **new** request — a real duplicate risk |
| Key used on a different endpoint | Keys are scoped per endpoint; mismatch errors |

Three consequences for your design:

1. **Keys must be generated at operation-creation time** (when the order row is written), not
   at request time, so every retry — browser, mobile, worker — presents the same key.
2. **24 h retention means your local key store outlives the provider's.** For retries beyond
   24 h, your own `idempotency_keys` table (key → order → last known provider status) is the
   only defense; the provider will happily execute a 25-hour-late retry as new.
3. **409 is not an error to surface** — it is a synchronization signal: wait briefly, then
   re-read the provider object (or your stored response) for the outcome.

```ts
// Local key ledger: outlives provider retention and survives provider swaps.
CREATE TABLE payment_idempotency (
  key             TEXT PRIMARY KEY,          -- e.g. "charge:ord_123"
  order_id        TEXT NOT NULL,
  request_hash    TEXT NOT NULL,             -- detect same-key-different-params
  provider_status TEXT NOT NULL DEFAULT 'in_flight',
  provider_id     TEXT,                      -- charge / PaymentIntent id once known
  last_error_code TEXT,
  created_at      TIMESTAMPTZ NOT NULL,
  updated_at      TIMESTAMPTZ NOT NULL
);
```

**Key data:** provider retention **24 h**; your ledger retains indefinitely (or until the
dispute window closes); `request_hash` = canonical JSON of the money-relevant params
(`orderId`, `amount`, `currency`) so a parameter change is caught locally *before* it becomes
a provider 400.

## Safe retries for financial ops (42.16)

A retry is safe for a financial operation only when **at least one** of these holds:

1. **The operation is provably unexecuted** — a definite, terminal-class request error
   (`invalid_request_error`) that the provider rejected before evaluation.
2. **The retry presents the same idempotency key** — the provider collapses duplicates, and
   your local ledger prevents the beyond-24h hole.
3. **The operation is read-only** — status queries are freely retryable.

Everything else routes to **reconciliation**, not retry. Concretely, the classification for a
Stripe-flavored client:

| Error class | Examples | Retry? | Mechanism |
| ----------- | -------- | ------ | --------- |
| Request rejected pre-evaluation | `invalid_request_error`, `parameter_missing` | ❌ | Fix code |
| Terminal outcome | `card_declined`, `expired_card`, `insufficient_funds`, `incorrect_cvc` | ❌ | User action |
| Action-required | `authentication_required` | ❌ (resume auth) | Client challenge flow |
| Rate limited | `rate_limit` (HTTP 429) | ✅ | Backoff + `Retry-After`, same key |
| Provider transient | `processing_error`, HTTP 5xx, connection reset **before** send | ✅ | Backoff, same key |
| Ambiguous (after send) | read timeout, 502/504, reset after send | ⚠️ | **Replay same key once**, then reconcile |
| Concurrent-key | HTTP 409 `idempotency_error` | ⚠️ | Wait + re-read stored outcome |

> ⚠️ **Hazard.** "Replay the same key once" on ambiguity is safe *because* the provider
> deduplicates. If you are between providers or the key is stale (>24 h), the replay **is** a
> new charge. In that window the only safe move is lookup-or-park.

## Resolving ambiguity: the decision procedure

```ts
async function resolveAmbiguousCharge(orderId: string): Promise<ChargeOutcome> {
  const row = await ledger.get(orderId);                       // our key + request hash
  if (row?.provider_id) return fromProvider(row.provider_id);  // already known

  // Same key still within provider retention → idempotent replay is safe.
  if (row && age(row.created_at) < 24 * 3600 * 1000) {
    const res = await stripe.charges.list({ limit: 100, starting_after: null,
      // filter server-side by our metadata
    }).catch(() => null);
    const hit = res?.data.find((c) => c.metadata?.orderId === orderId);
    if (hit) return { state: "succeeded", chargeId: hit.id };
    return { state: "failed_definite" };                        // provider says: nothing there
  }

  // Key too old or ledger missing → park for the reconciliation worker.
  await queue.enqueue("payment.verify", { orderId }, { delayMs: 60_000 });
  return { state: "pending_verification" };
}
```

The three terminal states of this procedure, all of which your UI and API must express:

| State | Meaning | Customer sees |
| ----- | ------- | ------------- |
| `succeeded` | Charge exists (found by replay or lookup) | Order confirmed |
| `failed_definite` | Provider confirms no charge | Payment failed — retry CTA |
| `pending_verification` | Still unknown | "Confirming your payment…" — **never** "failed" |

**Key data:** recommended verification schedule — retry the lookup with backoff for a few
minutes (the provider's `processing` usually settles quickly), then fall to a human-review
queue within **one business day**; money left in `pending_verification` longer than that is an
alert, because the dispute window is running.

## Worked example — the 502 that became three charges

A fintech's mobile client timed out at 30 s on capture (provider p99 was 35 s during a
promotion). The client retried with a new key generated per tap; the server obliged. Three
charges landed on one order. Postmortem findings: (1) keys were request-scoped, not
operation-scoped; (2) the server mapped provider 5xx to a generic `500`, which the client
treated as retryable-with-new-key; (3) there was no local key ledger, so nothing could detect
the duplication. Fixes: operation-scoped keys minted with the order; a client retry policy
that *reuses* the key; server-side `pending_verification` state; ledger-backed detection that
caught two more latent duplicates in the same cohort. Refund rate for the cohort dropped to
zero within a week.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Client-generated UUID per tap | Zero server work | Guarantees duplicates | Never for money |
| Server-minted key per order | Duplicate-safe | Requires order-first flow | ✅ Default |
| Provider-key only | No local state | 24h blind spot | Low volume + reconciliation |
| Ledger + provider keys | Auditable, replayable, swap-safe | One more table | Financial SaaS |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mint the key when the order is created | Mint it per HTTP attempt |
| Store the request hash with the key | Trust that "same key = same params" |
| Treat 409 as wait-and-re-read | Surface 409 as a payment failure |
| Park unknowns in `pending_verification` | Map ambiguous → "failed" |
| Keep a local ledger past 24 h | Rely on provider retention alone |
| Retry 429 honoring `Retry-After`, same key | Retry 429 with a new key |

## Common mistakes

- **Per-attempt keys** — the root cause of nearly every double-charge incident.
- **Mapping "error" to "failed" in the API layer** — throws away the ambiguity signal.
- **Replaying a stale key (>24 h) expecting dedupe** — provider executes it fresh.
- **Reconciliation that only looks at the last hour** — misses the slow-settling cases.
- **No request-hash check** — same key + changed amount becomes a provider 400 mid-incident.

## Checklist

- [ ] Payment idempotency keys are minted at order creation and reused by every client retry.
- [ ] A local key ledger outlives the provider's 24 h retention.
- [ ] Provider 409/`idempotency_error` maps to wait-and-re-read, not failure.
- [ ] Timeouts and 5xx-after-send map to `pending_verification`, never `failed`.
- [ ] A reconciliation worker drains `pending_verification` with lookup, then human review.
- [ ] Retry classification (retryable / action-required / terminal / ambiguous) lives in the
      registry and is tested.

## Related

- [Refunds, Subscription States, Quotas, and Entitlements](../01-concepts/03-refunds-subscription-states-and-entitlements.md)
- [Webhook Reconciliation and Safe Financial Retries](../03-practical-examples/02-webhook-reconciliation-and-safe-financial-retries.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
