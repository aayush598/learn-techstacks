# One Payment Provider Timeout, Six Languages

> Part XVIII · Chapter 47 · Sections 47.2–47.9, 47.14–47.16 (applied) · _Estimated reading time: 20 min_
> **Prerequisite:** [Native Chaining and Wrapping Capabilities](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md), [Type-Safe Handling and the Common Architecture](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)

## In one sentence

The Stripe capture request timed out after 2000 ms — the **same** failure, with the **same**
ambiguity about whether the charge was created — and the six implementations below show how
Go, Rust, Python, TypeScript, Java, and C# each encode it, preserve the cause, classify it,
and answer the only question that matters: **may the client retry?**

## Why this matters in production

A payment timeout is the hardest ordinary error in a SaaS product, because it is **ambiguous**:
the provider may have created the charge and lost the response, or may never have received it.
Retry without an idempotency key and you double-charge a customer; report it as a failure and
you hide a charge that succeeded. Handling it badly is expensive in both directions — a
double-charge generates refunds, support tickets, and chargebacks; a swallowed success creates
a subscription that was paid for and never activated.

Every language must therefore answer the same three questions identically:

1. **What code does this failure become?** (`PAYMENT_PROVIDER_TIMEOUT`)
2. **Is it retryable, and under what condition?** (retryable *only* with the same
   `Idempotency-Key`; the outcome is ambiguous until reconciled)
3. **What does the client get?** (a stable status + code + a correlation id, never a raw
   provider error)

## The shared contract

| Property | Value |
| -------- | ----- |
| Trigger | Stripe capture did not respond within the **2000 ms** provider deadline |
| Vendor detail | `request_id=req_9f2`, `elapsed_ms=2000` |
| App code | `PAYMENT_PROVIDER_TIMEOUT` |
| Category | external dependency · transient · **ambiguous outcome** |
| Retryable | **Yes — only with the same idempotency key** |
| HTTP status | `504` (a `503` is acceptable if you prefer "dependency unavailable") |
| Client action | retry the same request with the same `Idempotency-Key` |
| Alert | No (expected at <1% of captures) |
| Internal action | mark the attempt **pending**, reconcile later, never auto-retry the charge |

## Go

```go
// model + translation (adapter)
type PaymentError struct {
    Code      string
    Retryable bool
    Ambiguous bool          // ← the field that makes this error safe
    RequestID string
    err       error
}

func (e *PaymentError) Error() string { return e.Code }
func (e *PaymentError) Unwrap() error { return e.err }

func (a *StripeAdapter) Capture(ctx context.Context, amt int, idem string) (*Receipt, error) {
    r, err := a.client.Capture(ctx, amt, idem)
    if err != nil {
        var te *stripe.TimeoutError
        if errors.As(err, &te) {
            return nil, &PaymentError{Code: "PAYMENT_PROVIDER_TIMEOUT", Retryable: true,
                Ambiguous: true, RequestID: te.RequestID, err: err}
        }
        return nil, fmt.Errorf("stripe capture: %w", err)
    }
    return r, nil
}

// boundary — one writer of the response body
func WriteError(w http.ResponseWriter, err error, reqID string) {
    e := normalize(err)                     // → *PaymentError (errors.As)
    p := policyFor(e.Code)                  // → { status: 504, retryable: true }
    w.Header().Set("Content-Type", "application/problem+json")
    w.WriteHeader(p.status)
    _ = json.NewEncoder(w).Encode(problem(e, p, reqID))
}
```

**Go-specific note:** the ambiguity is data, not control flow. Because `Ambiguous` is a field on
the error, the retry policy can read it — and `errors.As` is the only way to get at it without
string matching.

## Rust

```rust
// model
#[derive(Debug, thiserror::Error)]
pub enum PaymentError {
    #[error("payment provider timed out after {elapsed_ms}ms")]
    ProviderTimeout {
        elapsed_ms: u64,
        ambiguous: bool,
        #[source]
        source: GatewayError,
    },
    #[error("payment failed")]
    Other {
        #[source]
        source: Box<dyn std::error::Error + Send + Sync>,
    },
}

// translation (adapter)
pub async fn capture(svc: &StripeAdapter, amt: i64, idem: &str) -> Result<Receipt, PaymentError> {
    svc.capture(amt, idem).await.map_err(|source| match source {
        GatewayError::Timeout { elapsed_ms, request_id } => PaymentError::ProviderTimeout {
            elapsed_ms,
            ambiguous: true,
            source: GatewayError::Timeout { elapsed_ms, request_id },
        },
        other => PaymentError::Other { source: Box::new(other) },
    })
}
```

**Rust-specific note:** the enum variant *is* the classification. `match` on
`PaymentError::ProviderTimeout { .. }` is exhaustive by construction, and `#[source]` keeps the
gateway error reachable for logging.

## Python

```python
# model
class PaymentError(AcmeError):
    def __init__(self, code: str, *, retryable: bool = False,
                 ambiguous: bool = False, **ctx):
        super().__init__(code, retryable=retryable, **ctx)
        self.ambiguous = ambiguous

# translation (adapter)
def capture(self, amount: int, idem: str) -> Receipt:
    try:
        return self._client.capture(amount, idempotency_key=idem)
    except stripe.error.APIConnectionError as exc:
        raise PaymentError(
            "PAYMENT_PROVIDER_TIMEOUT", retryable=True, ambiguous=True,
            provider_request_id=exc.request_id,
        ) from exc                       # ← cause preserved, traceback names it
```

**Python-specific note:** `from exc` is what makes the traceback say "direct cause" instead of
"during handling of the above exception". Without it, the vendor stack is still attached but
the semantics are wrong.

## TypeScript

```ts
// model — a discriminated union so `switch` is exhaustive
export type PaymentFailure =
  | { code: "PAYMENT_CARD_DECLINED"; retryable: false; ambiguous: false }
  | { code: "PAYMENT_PROVIDER_TIMEOUT"; retryable: true; ambiguous: true; providerRequestId: string }
  | { code: "PAYMENT_IDEMPOTENCY_CONFLICT"; retryable: false; ambiguous: false };

// translation (adapter)
export async function capture(amount: number, idem: string): Promise<Receipt> {
  try {
    return await stripe.paymentIntents.create({ amount }, { idempotencyKey: idem });
  } catch (err) {
    throw translateStripeError(err);     // returns a PaymentFailure, cause attached
  }
}

function translateStripeError(err: unknown): PaymentFailure {
  if (isStripeTimeout(err)) {
    return {
      code: "PAYMENT_PROVIDER_TIMEOUT", retryable: true, ambiguous: true,
      providerRequestId: err.requestId ?? "unknown",
    };
  }
  throw err;                             // unknown → propagate, never guess
}
```

**TypeScript-specific note:** the ambiguity is a literal in the type, so `plan(failure)` can
exhaustively branch and the compiler rejects a missing case. `unknown` in the `catch` forces
narrowing before any property access.

## Java

```java
// model — unchecked domain exception carrying structured metadata
public final class PaymentException extends RuntimeException {
    private final String code;
    private final boolean retryable;
    private final boolean ambiguous;
    private final String providerRequestId;

    public PaymentException(String code, boolean retryable, boolean ambiguous,
                            String providerRequestId, Throwable cause) {
        super(code, cause);                      // ← cause preserved natively
        this.code = code;
        this.retryable = retryable;
        this.ambiguous = ambiguous;
        this.providerRequestId = providerRequestId;
    }
    public String code() { return code; }
    public boolean retryable() { return retryable; }
    public boolean ambiguous() { return ambiguous; }
    public String providerRequestId() { return providerRequestId; }
}

// translation (adapter)
public Receipt capture(int amountCents, String idemKey) {
    try {
        return gateway.capture(amountCents, idemKey);
    } catch (StripeTimeoutException te) {
        throw new PaymentException("PAYMENT_PROVIDER_TIMEOUT", true, true,
                                   te.getRequestId(), te);
    }
}
```

**Java-specific note:** because the exception is unchecked, nothing forces the caller to
handle it — so the *only* enforcement is the boundary's `@ControllerAdvice`. If that advice
does not exist, the timeout escapes as a raw 500.

## C#

```csharp
// model
public sealed class PaymentException : Exception
{
    public string Code { get; }
    public bool Retryable { get; }
    public bool Ambiguous { get; }
    public string? ProviderRequestId { get; }

    public PaymentException(string code, bool retryable, bool ambiguous,
                            string? providerRequestId, Exception? inner) : base(code, inner)
    {
        Code = code; Retryable = retryable; Ambiguous = ambiguous;
        ProviderRequestId = providerRequestId;
    }
}

// translation (adapter)
public async Task<Receipt> CaptureAsync(int amountCents, string idemKey, CancellationToken ct)
{
    try
    {
        return await _gateway.CaptureAsync(amountCents, idemKey, ct);
    }
    catch (StripeTimeoutException ex)
    {
        throw new PaymentException("PAYMENT_PROVIDER_TIMEOUT", retryable: true,
                                   ambiguous: true, ex.RequestId, ex);
    }
}
```

**C#-specific note:** `TaskCanceledException` is ambiguous in .NET — it is thrown both for
caller cancellation *and* for `HttpClient` timeouts. The `catch` must check
`ct.IsCancellationRequested` before classifying a timeout as retryable; otherwise a client
disconnect is reported as a provider outage.

## Side-by-side

| Aspect | Go | Rust | Python | TypeScript | Java | C# |
| ------ | -- | ---- | ------ | ---------- | ---- | -- |
| Encoded as | struct + `error` interface | enum variant | exception class | discriminated union | exception class | exception class |
| Cause link | `Unwrap()` | `#[source]` | `__cause__` (`from`) | `cause` option (ES2022) | cause constructor | inner exception |
| "Ambiguous" flag | field | struct field | attribute | literal in the type | boolean field | property |
| Exhaustiveness | no | `match` | no | `switch` + `never` | sealed + `switch` (21) | no |
| Lint gate for ignoring errors | `errcheck` | `#[must_use]` | `mypy --strict` | `strict` + `no-floating-promises` | compiler (unchecked: none) | analyzer rules |
| Boundary | `http` middleware | tower layer | middleware | Express/NestJS | `@ControllerAdvice` | ASP.NET middleware |
| Enforcement that it is handled | `errcheck` in CI | compiler | none | none | none (unchecked) | none |
| Re-throw that keeps the stack | `fmt.Errorf("%w")` | `#[source]` | `from exc` | `cause` option | cause constructor | `throw;` / `ExceptionDispatchInfo` |

## Key data / numbers

- Stripe's own API guidance: **network errors and timeouts are safe to retry with the same
  idempotency key**; a `429` should be retried with exponential backoff; a `402` must not.
- HTTP **`504`** is the correct status for "an upstream gateway did not respond in time";
  **`503`** is the alternative when you prefer to signal "dependency unavailable". `502` is for
  a *malformed* upstream response — not for a timeout.
- Idempotency keys are stored by providers for **at least 24 hours** (Stripe documents 24 h) —
  so a client retry window longer than that can create a duplicate charge.
- Typical provider read timeouts: **2000 ms** (Stripe recommends 80 s for its own calls, but a
  checkout request should use a much shorter internal deadline so the client gets an answer).
- Recommended internal policy: **≤ 2 automatic retries** with the same key, then mark the
  attempt `pending` and reconcile via a webhook (`payment_intent.succeeded`) rather than by
  polling in the request path.
- Alerting threshold: provider timeouts above **1% of captures over 5 minutes** indicate a
  provider incident; below that they are noise.

## Real-world use case — Acme SaaS `Checkout`

Acme's checkout had three services — a TypeScript API, a Java billing service, and a Python
reconciliation worker — all calling the same provider. During a provider incident, all three
classified the timeout differently: TypeScript returned `500` (because `translateStripeError`
did not recognise the SDK's error shape), Java returned `503` with a generic
`PAYMENT_FAILED`, and Python marked the attempt `failed` and **retried the capture without an
idempotency key**. Result: 37 duplicate charges in 40 minutes, all requiring refunds, and the
Python worker's "failure" state hid four charges that had actually succeeded.

The fix was to make the *contract* identical rather than to patch each service:

1. One registry entry for `PAYMENT_PROVIDER_TIMEOUT`: `504`, `retryable: true`,
   `ambiguous: true`, `alert: false`.
2. One generated error type per language, so a timeout is a **typed variant**, not a string.
3. The `ambiguous` flag became part of the type in all three languages, so the retry policy
   could refuse to auto-retry a charge and instead write a `pending` attempt row for the
   reconciliation worker to resolve from the provider's webhook.

After the change, the same incident produced 37 attempts marked `pending`, **zero duplicate
charges**, and 37 clean reconciliations. The interesting part is that no service changed its
control flow — only the *shape* of the error and the data attached to it.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared registry + generated types | Identical behavior everywhere | Generator + codegen step | Multi-service products |
| Per-language hand-written types | No tooling | Diverges; the Acme incident | Single language |
| Ambiguity as a field on the error | Data-driven retry policy | Every consumer must honour it | Payment-like operations |
| Ambiguity as a separate outcome type | Impossible to ignore | More variants; noisier matches | Type-safe languages (Rust/Kotlin/TS) |
| Retry immediately on timeout | Fast recovery | Double-charge risk | Only with guaranteed idempotency |
| Mark pending + reconcile | No duplicates; truth converges | Slower UX; needs a reconciler | Any non-idempotent side effect |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Record ambiguity as explicit metadata | Treat a timeout as an ordinary retryable error |
| Retry only with the same idempotency key | Retry a capture with a fresh key |
| Keep the provider's request id in the error | Log only "payment timeout" |
| Use one registry entry across services | Let each service map the vendor error itself |
| Return `504`/`503` with a stable code | Return `500` for a dependency timeout |
| Re-throw unknown vendor errors unchanged | Guess a code for an unrecognized error |

## Common mistakes

- **The forgotten ambiguity.** The error is marked retryable, a generic retry helper fires, and
  the charge is duplicated. Fix: `retryable` and `ambiguous` are separate flags; the retry
  policy checks both.
- **The SDK-shape drift.** The vendor SDK renamed its timeout error between versions and the
  `instanceof`/`is`-check stopped matching; every timeout became an unknown error and a `500`.
  Fix: match on the provider's `code`/status, and have a tested "unknown vendor error" branch.
- **The provider request id dropped in translation.** The adapter wrapped the error but did not
  copy `request_id`; support tickets became unactionable. Fix: copy structured fields in the
  adapter, not just the cause.
- **.NET's `TaskCanceledException`.** Classified as a provider timeout when the *client* had
  disconnected. Fix: check `ct.IsCancellationRequested` first.
- **Python's missing `from`.** The vendor exception stayed attached as `__context__`, so the
  traceback implied the wrong relationship. Fix: `raise ... from exc`.
- **Go's `%v`.** `fmt.Errorf("stripe capture: %v", err)` flattened the cause, and the adapter's
  `errors.As` no longer matched. Fix: `%w` whenever the cause must stay inspectable.

## Checklist

- [ ] Does one registry entry describe this failure for every service?
- [ ] Is ambiguity recorded explicitly rather than inferred from "retryable"?
- [ ] Can a retry happen without an idempotency key? (It must not.)
- [ ] Is the provider's request id carried into logs and the internal error?
- [ ] Does an unrecognized vendor error propagate rather than become a guessed code?
- [ ] Is the client-facing status documented as `504`/`503` with a stable code?

## Related

- [Native Chaining and Wrapping Capabilities](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- [Type-Safe Handling and the Common Architecture](../02-deep-dive/02-type-safe-handling-and-common-architecture.md)
- [Chapter 42 — Auth, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
