# Handling Lost Responses and Retries Safely

> Part X · Chapter 26 · Sections 26.13–26.16 · _Estimated reading time: 16 min_

## In one sentence

**A worked example for Checkout: when a payment capture times out with ambiguity, resolve safely via idempotency and status lookup instead of blindly retrying.**

## Why this matters in production

Payment operations are non-idempotent by default and have financial impact. Read timeout after full request sent is ambiguous. This example shows the safe pattern used by **Acme SaaS**.

## Core concept

- **Detect ambiguity**: `requestSent=true`, `phase=read`, timeout/reset.
- **Don't blindly retry** if not safe.
- **Use idempotency key** — server deduplicates.
- **Query status** — determine actual remote state.
- **Handle three cases**: already captured, requires capture, unknown.

## Worked example

### Error detection
```ts
interface AmbiguousNetErr {
  ambiguous: boolean;
  phase: "read" | "write";
  requestSent: boolean;
  category: string;
}
```

### Safe capture
```ts
export async function safeCapturePayment(
  pay: PaymentProvider,
  paymentIntentId: string,
  orderId: string
): Promise<Result<{ captured: boolean; deduped: boolean }, AppErr>> {
  const idemKey = `capture:${paymentIntentId}:${orderId}`;
  try {
    const res = await pay.capturePayment(paymentIntentId, idemKey);
    return { ok: true, value: { captured: true, deduped: false } };
  } catch (e: unknown) {
    const ne = e as AmbiguousNetErr;
    if (ne.ambiguous && ne.phase === "read" && ne.requestSent) {
      // Resolve ambiguity
      const st = await pay.getPaymentStatus(paymentIntentId);
      if (st.status === "succeeded" || st.status === "captured") {
        return { ok: true, value: { captured: true, deduped: true } };
      }
      if (st.status === "requires_capture") {
        // Retry safely with same idempotency key
        const res2 = await pay.capturePayment(paymentIntentId, idemKey);
        return { ok: true, value: { captured: true, deduped: false } };
      }
      if (st.status === "processing") {
        return { ok: false, error: new AppErr("PAYMENT_PROCESSING", { retryable: true }) };
      }
      // Unknown state
      return { ok: false, error: new AppErr("PAYMENT_STATE_UNKNOWN", { retryable: false, uncertain: true }) };
    }
    // Not ambiguous - propagate
    throw e;
  }
}
```

### Usage in Checkout
```ts
async function checkout(orderId: string, piId: string) {
  const r = await safeCapturePayment(payments, piId, orderId);
  if (!r.ok) {
    const err = r.error;
    if (err.code === "PAYMENT_STATE_UNKNOWN") {
      await db.markOrderUncertain(orderId);
      // Reconciliation will resolve later
      return { status: "pending_verification" };
    }
    throw err;
  }
  const v = r.value;
  await db.markOrderPaid(orderId, { deduped: v.deduped });
  return { status: "paid" };
}
```

**Key data:**
- `PAYMENT_STATE_UNKNOWN` is marked uncertain for reconciliation.
- Deduped flag tracks idempotent replays.

## Real-world use case

**Checkout**: read timeout occurs after capture request sent. Status lookup shows `succeeded` — order marked paid, no double charge. If status is `requires_capture`, retry with same idempotency key succeeds (or returns previous result). If truly unknown, order goes to uncertain state for manual/reconciliation processing.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Status lookup** | Immediate resolution | Requires provider API | **Recommended** |
| **Reconciliation only** | Works if no lookup | Delayed | Fallback |
| **No handling** | Simple | Dangerous | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use idempotency keys before any retry | Retry without keys |
| Check status on ambiguity | Assume |
| Track uncertain outcomes | Lose state |
| Prefer status lookup over blind retry | Blind retry |

## Common mistakes

- **No status endpoint** — can't resolve safely.
- **Forgetting idempotency key** — retry creates new request.
- **Not recording deduped** — audit trail incomplete.

## Checklist

- [ ] Ambiguity condition checked precisely.
- [ ] Idempotency key includes stable identifiers.
- [ ] Status lookup handles all provider states.
- [ ] Uncertain case leads to reconciliation path.
- [ ] Audit trail records deduplication.

## Related

- [Ambiguous Remote Outcomes](../02-deep-dive/02-ambiguous-remote-outcomes.md)
- [Ambiguous Outcomes and Service Boundaries](../01-concepts/04-ambiguous-outcomes-and-service-boundaries.md)
- [Stripe Error Mapping Adapter](../../25-third-party-api-error-handling/03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../../GLOSSARY.md)
