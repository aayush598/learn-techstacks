# Fallbacks for Optional vs Critical Dependencies

> Part X · Chapter 25 · Section 25.17, 25.18 · _Estimated reading time: 14 min_

## In one sentence

**Decide fallback behavior by dependency criticality**: for optional dependencies degrade gracefully, for critical dependencies fail closed and never guess at consistency.

## Why this matters in production

**Acme SaaS Checkout** must not proceed if payment capture fails; but if address validation fails, it can often proceed with degraded validation. **AgentRun** may fall back to a different model provider if the primary is unavailable. Explicit policies prevent dangerous "fail open" choices for critical flows.

## Core concept

| Dependency type | Examples | On failure | Do |
| --------------- | -------- | ---------- | --- |
| **Critical** | Payment capture, auth, DB writes affecting money/state | **Fail closed** | Return explicit error; don't mark order paid; use idempotency; queue for recovery |
| **Optional** | Address validation, recommendation API, analytics | **Degrade** | Return cached/default value, log warning, proceed if safe |

## How it works

### Decision rules
- **Can the business operation complete safely without this?** If no → critical.
- **Will proceeding corrupt state or risk money/data loss?** If yes → critical, fail closed.
- **Is there a safe fallback (cache, default, skip)?** If yes and non-critical → degrade.

### Implementation patterns
- **Try/catch with explicit classification** — only degrade for known optional failures.
- **Feature flags** — quickly disable optional features during outages.
- **Staleness indicators** — if using cached fallback, communicate degradation to user (if relevant).

## Worked example

### Optional dependency
```ts
async function enrichCheckout(address: Address) {
  try {
    const v = await addressService.validate(address);
    return { ...address, validated: true, score: v.score };
  } catch (e) {
    // degrade: proceed without full validation
    logger.warn("address_validation_unavailable", { err: classify(e) });
    return { ...address, validated: false, degraded: true };
  }
}
```

### Critical dependency
```ts
async function captureOrder(orderId: string) {
  const r = await payments.capture(orderId, idem(`capture:${orderId}`));
  if (!r.ok) {
    const code = r.error.code;
    if (code === AcmeErr.UPSTREAM_UNAVAILABLE || code === AcmeErr.UPSTREAM_TIMEOUT) {
      // fail safely - don't mark paid
      await db.setPending(orderId, "payment_provider_unavailable");
      throw new AppError("PAYMENT_UNAVAILABLE", { retryable: false });
    }
    if (code === AcmeErr.UPSTREAM_DECLINED) {
      await db.setFailed(orderId, "declined");
      throw new AppError("PAYMENT_DECLINED", { retryable: false });
    }
    await db.setFailed(orderId, "unknown");
    throw new AppError("PAYMENT_FAILED", { retryable: false });
  }
  await db.setPaid(orderId, r.value.id);
}
```

**Key data:**
- **Fail closed**: never assume success on timeout for critical ops.
- **Degrade only** when safe; log with classification.

## Real-world use case

**Acme SaaS — Checkout during Stripe outage:** Address validation (optional) degrades; payment capture (critical) fails closed with `PAYMENT_UNAVAILABLE`. The UI tells user to try again. No order is marked paid. This prevents financial inconsistency.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Always fail closed** | Safe | Unnecessary UX friction for optional deps | Only for critical |
| **Selective degrade** | Good UX, safe if correct | Requires classification | **Recommended** |
| **Always degrade** | Resilient | Dangerous for money/state | **Never** for critical |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Document critical vs optional per dependency | Treat all same |
| Fail closed for payment/auth/state changes | Guess and proceed on critical failures |
| Degrade only when no consistency risk | Degrade billing flows |
| Log degradation with classification | Silent degradation |
| Use feature flags to disable optional features | Can't control during incidents |

## Common mistakes

- **Fail open by default:** Proceeding on timeout after sending money request.
- **Creeping criticality:** Optional becomes critical over time without policy change.
- **Silent degradation:** Users don't know why data looks incomplete.

## Checklist

- [ ] Critical vs optional list exists for all external deps.
- [ ] Fallback logic tested for each class.
- [ ] Critical ops fail closed on ambiguity.
- [ ] Optional ops degrade with warnings logged.
- [ ] Feature flags allow disabling optional deps.

## Related

- [Translation, Adapters, and Outages](../01-concepts/04-translation-adapters-and-outages.md)
- [Adapters, Vendor Outages, and Replaceability](../02-deep-dive/03-adapters-vendor-outages-and-replaceability.md)
- [Stripe Error Mapping Adapter](./01-stripe-error-mapping-adapter.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Glossary](../../../GLOSSARY.md)
