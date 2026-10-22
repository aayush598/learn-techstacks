# Stripe Error Mapping Adapter

> Part X · Chapter 25 · Section 25.2, 25.3, 25.6, 25.14, 25.15 · _Estimated reading time: 18 min_

## In one sentence

**A worked example showing how to translate Stripe errors to stable internal errors at the adapter boundary** for **Checkout** operations, preserving retryability and never leaking vendor types.

## Why this matters in production

**Checkout** needs to create payment intents and capture charges. Stripe returns rich error objects; we must normalize them to `AcmeErr` codes, respect `Retry-After` on rate limits, handle `api_connection_error` as retryable (if idempotent), and treat `card_declined` as non-retryable with user-safe messaging.

## Core concept

- **Adapter owns Stripe SDK** — domain imports `PaymentProvider` interface only.
- **Normalize + map** — extract common fields, use mapping table.
- **Classify retryability** — card errors non-retryable, rate limits retryable with delay, connection errors retryable.
- **Idempotency** — pass idempotency keys for POSTs.
- **Safe messages** — user sees generic message; details in logs.

## Worked example

### Internal error codes
```ts
export enum AcmeErr {
  UPSTREAM_AUTH_INVALID = "UPSTREAM_AUTH_INVALID",
  UPSTREAM_FORBIDDEN = "UPSTREAM_FORBIDDEN",
  UPSTREAM_RATE_LIMITED = "UPSTREAM_RATE_LIMITED",
  UPSTREAM_DECLINED = "UPSTREAM_DECLINED",
  UPSTREAM_INVALID_REQUEST = "UPSTREAM_INVALID_REQUEST",
  UPSTREAM_UNAVAILABLE = "UPSTREAM_UNAVAILABLE",
  UPSTREAM_TIMEOUT = "UPSTREAM_TIMEOUT",
  UPSTREAM_MALFORMED = "UPSTREAM_MALFORMED",
  UPSTREAM_UNKNOWN = "UPSTREAM_UNKNOWN",
}
```

### Stripe adapter
```ts
import Stripe from "stripe";

export class StripePaymentAdapter implements PaymentProvider {
  private stripe: Stripe;
  constructor(key: string) { this.stripe = new Stripe(key, { apiVersion: "2024-06-20" }); }

  async createPaymentIntent(input: IntentInput, idemKey: string): Promise<Result<Intent, InternalErr>> {
    try {
      const pi = await this.stripe.paymentIntents.create({
        amount: input.amount,
        currency: input.currency,
      }, { idempotencyKey: idemKey });
      return { ok: true, value: mapPi(pi) };
    } catch (e) {
      return { ok: false, error: mapStripeError(e) };
    }
  }

  async capturePayment(id: string, idemKey: string): Promise<Result<Capture, InternalErr>> {
    try {
      const ch = await this.stripe.paymentIntents.capture(id, {}, { idempotencyKey: idemKey });
      return { ok: true, value: mapCapture(ch) };
    } catch (e) {
      return { ok: false, error: mapStripeError(e) };
    }
  }
}
```

### Mapping
```ts
function mapStripeError(e: unknown): InternalErr {
  // Stripe errors have type/code
  if (isStripeError(e)) {
    const err = e as Stripe.errors.StripeError;
    // Card errors
    if (err.type === "StripeCardError") {
      return new InternalErr(AcmeErr.UPSTREAM_DECLINED, {
        retryable: false,
        cause: err,
        vendorCode: err.code, // e.g. card_declined
      });
    }
    // Rate limit
    if (err.type === "StripeRateLimitError") {
      const retryAfterSec = parseRetryAfter(err.headers?.["retry-after"]);
      return new InternalErr(AcmeErr.UPSTREAM_RATE_LIMITED, {
        retryable: true,
        retryAfterSec,
        cause: err,
      });
    }
    // Auth
    if (err.type === "StripeAuthenticationError") {
      return new InternalErr(AcmeErr.UPSTREAM_AUTH_INVALID, { retryable: false, cause: err });
    }
    // Connection
    if (err.type === "StripeConnectionError") {
      return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true, cause: err });
    }
    // API errors
    if (err.type === "StripeAPIError") {
      return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true, cause: err });
    }
    // Invalid request
    if (err.type === "StripeInvalidRequestError") {
      return new InternalErr(AcmeErr.UPSTREAM_INVALID_REQUEST, { retryable: false, cause: err });
    }
  }
  // Network/unknown
  if (isNetworkError(e)) {
    return mapNetworkError(e); // see Chapter 26
  }
  return new InternalErr(AcmeErr.UPSTREAM_UNKNOWN, { retryable: false, cause: e });
}

function isStripeError(e: unknown): e is Stripe.errors.StripeError {
  return typeof e === "object" && e !== null && "type" in e && (e as any).type?.startsWith("Stripe");
}
```

### Usage in Checkout
```ts
async function checkoutCharge(orderId: string, amount: number) {
  const idemKey = `charge:${orderId}`;
  const res = await paymentProvider.createPaymentIntent({ amount, currency: "usd" }, idemKey);
  if (!res.ok) {
    const err = res.error;
    if (err.code === AcmeErr.UPSTREAM_DECLINED) {
      await db.updateOrder(orderId, { status: "payment_failed" });
      throw new UserError("Payment declined. Please use a different card.");
    }
    if (err.code === AcmeErr.UPSTREAM_RATE_LIMITED) {
      // retry with backoff respecting retryAfterSec
      throw new RetryableError(err.retryAfterSec);
    }
    if (err.code === AcmeErr.UPSTREAM_UNAVAILABLE) {
      throw new DependencyError("Payment provider temporarily unavailable.");
    }
    throw new InternalError("Payment failed.");
  }
  // proceed...
}
```

**Key data:**
- **`Retry-After`** parsed from Stripe headers when present.
- **Idempotency keys** passed for mutating operations.
- **Vendor types never exported** from adapter.
- **User-safe messages** separate from internal errors.

## Real-world use case

**Acme SaaS Checkout:** During peak traffic, Stripe returns `rate_limit_error`. The adapter maps to `UPSTREAM_RATE_LIMITED` with `retryAfterSec: 5`. The retry policy (Part XI) uses jittered exponential backoff respecting `Retry-After`, preventing retry storms. A card decline maps to non-retryable `UPSTREAM_DECLINED` and the UI shows a clear message without exposing Stripe internals.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Catch all, throw generic** | Simple | Loses retryability, bad UX | Never |
| **Map per error type** | Precise | Need to track Stripe error types | **Recommended** |
| **Table-driven** | Maintainable | Still need Stripe-specific keys | **Recommended** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pass idempotency keys to mutating calls | Retry non-idempotent calls without keys |
| Respect `Retry-After` on rate limits | Ignore throttling |
| Return `Result` or internal errors only | Let Stripe errors bubble to controllers |
| Separate user-safe messages from internal details | Expose `err.message` from Stripe to users |
| Pin Stripe API version | Use default/latest without pinning |

## Common mistakes

- **No idempotency:** Retrying `capture` without key risks double charge.
- **Retrying card declines:** Wastes resources, bad UX.
- **Leaking decline codes:** Showing raw Stripe decline codes to users.
- **Not handling network errors:** `StripeConnectionError` needs separate mapping.

## Checklist

- [ ] Adapter implements `PaymentProvider` interface.
- [ ] All Stripe error types mapped to internal codes.
- [ ] `Retry-After` parsed and passed.
- [ ] Idempotency keys used for creates/captures.
- [ ] User-safe messages defined; vendor details in logs only.
- [ ] Tests cover card_declined, rate_limit, api_connection_error.

## Related

- [Provider Error Translation Mechanics](../02-deep-dive/01-provider-error-translation-mechanics.md)
- [Fallbacks for Optional vs Critical Dependencies](./02-fallbacks-for-optional-vs-critical-dependencies.md)
- [Chapter 26 — Network Error Classification](../../26-network-and-distributed-communication-errors/03-practical-examples/01-network-error-classification-code.md)
- [Glossary](../../../GLOSSARY.md)
