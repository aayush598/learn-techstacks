# Adapters, Vendor Outages, and Replaceability

> Part X · Chapter 25 · Section 25.17, 25.18, 25.19, 25.20 · _Estimated reading time: 16 min_

## In one sentence

**Design adapters as replaceable boundaries with explicit outage behavior**: define critical vs optional dependencies, fail safely, and contain vendor incidents with timeouts/circuit breakers/budgets.

## Why this matters in production

When a vendor has a regional outage, **Checkout** must not create unpaid orders in "processing forever" state or retry in a tight loop. **WebhookIngest** may need to queue events. **AgentRun** may need to fall back to another model provider. Replaceable adapters make this possible without rewriting domain logic.

## Core concept

| Strategy | When | Behavior |
| -------- | ---- | -------- |
| **Fallback for optional deps** | Address validation, analytics, enrichment | Return cached/default or skip; don't block critical flow. |
| **Fail safely for critical deps** | Payment capture, authz checks | Fail closed with explicit error; don't guess; preserve consistency. |
| **Vendor outages** | Widespread failures | Timeouts, circuit breaker open, feature flag, queue with backpressure. |
| **Replaceable adapters** | Multi-vendor or migration | Interface-based, translation per vendor, contract tests. |

## How it works

### Adapter interface
```ts
interface PaymentProvider {
  createPaymentIntent(input: IntentInput): Promise<Result<Intent, InternalErr>>;
  capturePayment(id: string, idempotencyKey: string): Promise<Result<Capture, InternalErr>>;
}
```
- Returns `Result` or throws internal errors only.
- No vendor types in method signatures visible to domain.
- Idempotency keys passed explicitly.

### Critical vs optional
- **Critical**: Failure means you cannot complete the business operation safely. Example: cannot charge card → cannot mark order paid.
- **Optional**: Failure degrades experience but operation can complete. Example: cannot fetch recommendations → show empty list.

### Outage containment
- **Per-request timeouts** (connect/read) — see Chapter 26.
- **Circuit breaker**: Track failures; open after threshold; half-open with probe.
- **Retry budgets**: Limit retries per second across fleet.
- **Bulkheads**: Separate connection pools/threads per vendor.
- **Feature flags**: Disable vendor quickly.

## Worked example

```ts
// Critical: Checkout payment capture - fail closed
async function captureOrder(orderId: string) {
  const idem = `capture:${orderId}`;
  const res = await paymentProvider.capturePayment(orderId, idem);
  if (res.ok) {
    await db.markOrderPaid(orderId);
    return { ok: true };
  }
  const err = res.error;
  if (err.code === AcmeErr.UPSTREAM_UNAVAILABLE) {
    // Critical dep unavailable - fail safely, don't mark paid
    await db.markOrderPaymentPending(orderId, { reason: err.code });
    throw new InternalErr("PAYMENT_PROVIDER_UNAVAILABLE", { retryable: false, userSafe: "Payment temporarily unavailable, please try again." });
  }
  if (err.code === AcmeErr.UPSTREAM_DECLINED) {
    await db.markOrderPaymentFailed(orderId);
    throw new InternalErr("PAYMENT_DECLINED", { retryable: false, userSafe: "Payment declined." });
  }
  // ...
}

// Optional: address validation - degrade
async function validateAddress(addr: Address) {
  try {
    const r = await addressProvider.validate(addr);
    return r.ok ? r.value : { valid: true, degraded: true };
  } catch (e) {
    // degrade gracefully
    return { valid: true, degraded: true, warning: "address_verification_unavailable" };
  }
}
```

**Key data:**
- **Idempotency keys** required for non-idempotent critical operations.
- **Circuit breaker states**: closed/open/half-open.
- **Timeouts**: connect (e.g. 2s), read (e.g. 5s) — tune per dependency.

## Real-world use case

**Acme SaaS — Vendor outage playbook:** Stripe experiences outage. Circuit breaker opens for payment provider. **Checkout** stops retrying aggressively, returns `PAYMENT_PROVIDER_UNAVAILABLE` with a safe message, and marks orders as pending (not paid). **WebhookIngest** continues processing webhooks but payment-related actions are queued. **ExportJob** unaffected if not using Stripe. Once half-open probe succeeds, circuit closes gradually.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Hardcoded vendor** | Fast to build | Unswappable, hard to add fallbacks | Avoid for anything non-trivial |
| **Adapter per vendor with interface** | Replaceable, testable | More abstraction | **Recommended** |
| **Multi-vendor with routing** | High availability | Complex (consistency, reconciliation) | Advanced; need strong contracts |
| **Always retry on outage** | Seems resilient | Causes retry storms, wastes resources | **Never** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define critical vs optional per dependency | Treat everything as critical |
| Fail closed when cannot guarantee consistency | Mark order paid without confirmed charge |
| Use circuit breakers + retry budgets on outages | Retry in tight loop |
| Make adapters replaceable via interfaces | Import vendor SDKs in domain services |
| Have feature flags to disable vendors quickly | Require deployment to disable a failing vendor |

## Common mistakes

- **Fail open on critical ops:** Proceeding without confirmation risks double charges or unpaid orders.
- **No idempotency during retries:** Outage recovery causes duplicates.
- **Shared resources:** One vendor exhausting connection pool affects others.
- **Premature abstraction:** Over-engineering for vendors you'll never swap.

## Checklist

- [ ] PaymentProvider/StorageProvider/etc interfaces defined.
- [ ] Each call site knows if dependency is critical or optional.
- [ ] Outage behavior tested (circuit open, timeouts).
- [ ] Feature flag to disable failing vendor exists.
- [ ] Contract tests for adapters; can swap implementations.
- [ ] Idempotency keys used for non-idempotent critical operations.

## Related

- [Translation, Adapters, and Outages (Concepts)](../01-concepts/04-translation-adapters-and-outages.md)
- [Stripe Error Mapping Adapter](../03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Fallbacks for Optional vs Critical Dependencies](../03-practical-examples/02-fallbacks-for-optional-vs-critical-dependencies.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Glossary](../../../GLOSSARY.md)
