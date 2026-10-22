# Distributed Idempotency and Storage

> Part XI · Chapter 28 · Sections 28.6, 28.14, 28.15 · _Estimated reading time: 19 min_
> **Prerequisite:** [Idempotency Key Lifecycle](./01-idempotency-key-lifecycle.md)

## In one sentence

In a distributed system, idempotency becomes a **storage and propagation problem**: where the
key-to-result mapping lives, how it stays consistent with the side effect, and how the key travels
so every service dedupes against the same intent.

## Why this matters in production

A single-service key store is straightforward: one database, one transaction. Add a queue, a second
service, and an external provider, and the atomicity disappears. Teams then discover that "we check
Redis before charging" is not a guarantee — Redis and Postgres can disagree, the process can die
between them, and a child service never saw the key at all. This file covers the storage choices and
the propagation patterns that keep the guarantee intact.

## Storage choices

### Option 1 — Same database as the side effect (strongest)

```text
BEGIN
  INSERT idempotency_keys(...)
  INSERT charges(...)
COMMIT
```

**Pros:** atomic; a crash cannot leave the key and effect inconsistent.
**Cons:** only works for local effects. External provider calls cannot join the transaction.

### Option 2 — Outbox (external effects)

```text
BEGIN
  INSERT idempotency_keys(state=in_progress)
  INSERT outbox(event=ChargeRequested, key=K, payload)
COMMIT
   │
   └─▶ worker reads outbox, calls provider with K, writes outcome
```

**Pros:** reliable handoff; retries are safe; crash recovery is built in.
**Cons:** eventual completion; needs an outbox worker and status endpoint.

### Option 3 — Redis / dedicated store

```text
SET key:K "{state:in_progress}" NX EX 86400
```

**Pros:** fast, built-in TTL, simple.
**Cons:** not atomic with the DB side effect; a crash between Redis and the DB creates a gap; Redis
eviction can silently drop keys.

> ⚠️ **Hazard.** Using Redis with `allkeys-lru` can evict an idempotency key under memory pressure,
> re-enabling duplicates exactly when the system is already stressed. Use `noeviction` or a dedicated
> instance for keys.

### Option 4 — Provider-native (for the provider boundary)

Pass your key to Stripe/Adyen/etc. and let them dedupe. This protects the provider call but not your
own database writes. Use it **in addition to** your store, not instead of it.

### Storage comparison

| Store | Atomic with side effect | TTL | Survives crash | Best for |
| ----- | ----------------------- | --- | -------------- | -------- |
| Postgres (same tx) | Yes | Manual/job | Yes | Local writes |
| Outbox + Postgres | Yes (intent) | Manual/job | Yes | External calls |
| Redis | No | Native | Depends on persistence | Low-value, fast dedup |
| DynamoDB | No (unless single-table) | Native | Yes | High-scale services |
| Provider | N/A | Provider-defined | Provider-managed | Provider calls only |

## The consistency gap

Any design that writes the key in store A and the effect in store B has a window where they
disagree. The two failure directions:

| Gap | Consequence | Mitigation |
| --- | ----------- | ---------- |
| Key written, effect not | Retry blocked or replays a lie | `unknown` state + reconciliation |
| Effect written, key not | Duplicate on retry | Write key first, in the same tx if possible |

The safest ordering is **claim the key before the effect**, then commit the outcome. If you crash
after claiming but before the effect, the lease/sweeper marks it unknown and reconciliation proceeds.
If you crash after the effect but before completion, the same path resolves it.

## Propagating keys across services

### Pattern A — Propagate the original key

```text
client K → API K → Order K → Payment K
```

Every service stores `(service, K)` → result. Simple, but keys must be namespaced per service to
avoid cross-service collisions, and every service must implement the lifecycle.

### Pattern B — Deterministic child keys

```text
parent K
  ├─ K:payment
  ├─ K:inventory
  └─ K:email:<message_id>
```

Child keys are reproducible from the parent; a retried parent produces the same children, so each
service dedupes independently. This is the most robust pattern for workflows.

### Pattern C — Central idempotency service

A dedicated service owns the mapping and exposes `claim(key)`, `complete(key, result)`,
`get(key)`. Every caller consults it.

**Pros:** one implementation, one lifecycle.
**Cons:** network hop, availability dependency, potential bottleneck. Never put it on the critical
path without a fallback.

### Pattern D — Event-carried key

Events include the key in their envelope; consumers dedupe on it.

```json
{
  "event_id": "evt_8f2c",
  "idempotency_key": "K:payment",
  "type": "PaymentCaptured",
  "data": { "charge_id": "ch_1", "amount": 5000 }
}
```

Consumers store processed keys before applying effects. Combined with at-least-once delivery, this
gives an effectively exactly-once *effect* (Chapter 33).

## Distributed unknown outcomes

When a workflow spans services and one step's outcome is unknown, the reconciliation must identify
which step and which key. Store enough context to do that:

```text
workflow_id, parent_key, step, child_key, provider_ref, last_attempt_at
```

Then the reconciler can:

1. Query the provider/service by `child_key`.
2. Resolve to completed/retryable/terminal.
3. Emit the resolved event exactly once (idempotently).
4. Let downstream consumers dedupe on the event key.

## Worked example — a saga with child keys

```text
Checkout workflow K = order_42
  1. K:reserve-inventory  → Inventory service (dedup on child key)
  2. K:charge             → Payment service → Stripe (same child key)
  3. K:grant-entitlement  → Entitlements service
  4. K:send-receipt       → Notifications (K:email:receipt_42)

If step 2 times out:
  - Payment marks K:charge unknown, stores Stripe ref.
  - Reconciler queries Stripe by K:charge.
  - On success, emits PaymentCaptured {key: K:charge}.
  - Steps 3 and 4 dedupe on their own child keys; no duplicate grants or emails.
```

## Key data / numbers

- Redis key TTL: `EX 86400` (24h) mirrors typical payment retention.
- Outbox poll interval: 100ms–1s; batch size 100–1,000.
- Reconcile lookback: at least the provider's consistency window (seconds to minutes).
- Key namespaces: one per service (`billing:K`, `inventory:K`) to avoid collisions.
- Child key separator: `:` with deterministic, URL-safe encoding.
- Alert on: keys older than TTL still `in_progress`; provider effects with no key row.

## Real-world use case — Acme SaaS

Acme introduced a second service (Entitlements) that consumed `SubscriptionUpgraded` events but did
not dedupe. The Billing service retried event publication after a broker timeout, and Entitlements
granted the feature twice, resetting a usage counter. The team moved to child keys (`K:entitlement`)
and event envelopes carrying `idempotency_key`; Entitlements stored processed keys before applying
grants. Replays became harmless, and the incident category disappeared from the postmortem rotation.

## Trade-offs

| Pattern | Consistency | Complexity | Use when |
| ------- | ----------- | ---------- | -------- |
| Same-DB key | Strong | Low | Local side effects |
| Outbox | Strong (eventual) | Medium | External calls |
| Redis | Weak | Low | High-volume, low-risk |
| Propagated key | Per-service | Medium | Small number of services |
| Child keys | Per-service | Medium | Workflows, sagas |
| Central service | Strong | High | Many services, strict needs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put the key in the same DB when possible | Split key and effect across stores casually |
| Use an outbox for external calls | Commit the effect before the key |
| Namespace keys per service | Share one global key namespace |
| Derive child keys deterministically | Generate random child keys |
| Include keys in event envelopes | Rely on consumers to infer identity |
| Configure Redis without eviction for keys | Use `allkeys-lru` for idempotency data |

## Common mistakes

- **Assuming a central store is always available** and putting it on the hot path unguarded.
- **Writing the effect before the key**, so a crash enables duplicates.
- **Forgetting to namespace keys**, causing cross-service collisions.
- **Child keys that include timestamps**, breaking determinism.
- **No reconciliation across services**, leaving unknown outcomes unresolved.

## Checklist

- [ ] The key store is chosen deliberately (same DB, outbox, Redis, provider).
- [ ] Key claim happens before the side effect.
- [ ] External calls use an outbox or reconciler.
- [ ] Keys are namespaced per service.
- [ ] Child keys are deterministic.
- [ ] Events carry the idempotency key.
- [ ] Redis used for keys has eviction disabled.
- [ ] Unknown outcomes are reconciled by key.

## Related

- [Idempotency Key Lifecycle](./01-idempotency-key-lifecycle.md)
- [Idempotency in Payments, Jobs, and Webhooks](../01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
