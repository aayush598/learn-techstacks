# Normalization with the Recurring Cast

> Part VI · Chapter 16 · All sections · _Estimated reading time: 20 min_
> **Prerequisite:** [Why Translate and Normalize](../01-concepts/01-why-translate-and-normalize.md)

## In one sentence

This example normalizes errors from **four different dialects** — Stripe (payments), S3 (storage),
an LLM provider (AgentRun), and the OS (network) — into a **single `AppError` shape** used
uniformly by the retry engine, the HTTP mapper, and the job boundary.

## Why this matters in production

Acme's recurring cast touches four external systems in one workflow: a `Checkout` charges via
Stripe, `ExportJob` writes to S3, `AgentRun` calls an LLM and tools, and everything sits behind an
HTTP API. Before normalization, each consumer `switch`ed on a different vendor format. After
normalization, adding a provider or changing retry policy is a one-line change.

## The canonical shape

```ts
interface AppError {
  code: string;               // stable: PAYMENT_CARD_DECLINED, STORAGE_THROTTLED, ...
  category: Category;         // VALIDATION|AUTH|CONFLICT|DEPENDENCY|BUSINESS|RESOURCE|INTERNAL
  transient: boolean;
  httpStatus?: number;
  safeMessage: string;
  retryAfterMs?: number;
  meta: Record<string, unknown>; // requestId, tenantId, provider (internal only)
  cause?: unknown;            // ORIGINAL, server-side only
}
```

## Dialect 1 — Stripe (Checkout)

Stripe reports `error.type` and sometimes `error.code`; card declines arrive as HTTP `402`.

```ts
function fromStripe(e: Stripe.StripeRawError): AppError {
  switch (e.type) {
    case "card_error":
      return app("PAYMENT_CARD_DECLINED", "BUSINESS", false, 402, "Your card was declined.",
                 { provider: "stripe", stripeCode: e.code });
    case "rate_limit_error":
      return app("PAYMENT_RATE_LIMITED", "DEPENDENCY", true, 429,
                 "The payment provider is busy; retrying.", { provider: "stripe" },
                 retryAfterMsFrom(e));
    case "api_connection_error":
      return app("PAYMENT_UNAVAILABLE", "DEPENDENCY", true, 503,
                 "The payment provider is unavailable.", { provider: "stripe" });
    case "authentication_error":
      return app("PAYMENT_AUTH_FAILED", "INTERNAL", false, 500,
                 "Payment configuration error.", { provider: "stripe", alert: true });
    default:
      return unknown("stripe", e);
  }
}
```

## Dialect 2 — S3 (ExportJob)

AWS returns XML with a `<Code>`; the SDK surfaces it as `err.name`/`err.Code`.

```go
func fromS3(err error) *AppError {
    var ae smithy.APIError
    if errors.As(err, &ae) {
        switch ae.ErrorCode() {
        case "SlowDown":
            return app("STORAGE_THROTTLED", Dependency, true, 503, "Storage is throttled.", 1000, err)
        case "RequestTimeout":
            return app("STORAGE_TIMEOUT", Dependency, true, 504, "Storage timed out.", 0, err)
        case "NoSuchKey":
            return app("OBJECT_NOT_FOUND", NotFound, false, 404, "The object does not exist.", 0, err)
        case "AccessDenied":
            return app("STORAGE_ACCESS_DENIED", Internal, false, 500, "Storage access failed.", 0, err)
        }
    }
    return unknown("s3", err)
}
```

## Dialect 3 — LLM provider (AgentRun)

Provider errors distinguish **retryable** overload from **permanent** context/token limits.

```python
def from_llm(err) -> AppError:
    status = getattr(err, "status_code", None)
    body = getattr(err, "body", {}) or {}
    ptype = body.get("error", {}).get("type") or body.get("type")

    if status == 429 or ptype in ("rate_limit_exceeded", "rate_limit_error"):
        return app("LLM_RATE_LIMITED", "DEPENDENCY", True, 429,
                   "The model is rate limited; retrying.", retry_after_ms=2000, cause=err)
    if ptype in ("context_length_exceeded", "string_too_long"):
        return app("TOKEN_LIMIT_EXCEEDED", "BUSINESS", False, 422,
                   "The request exceeded the context window.", cause=err)
    if ptype in ("invalid_api_key", "authentication_error"):
        return app("LLM_AUTH_FAILED", "INTERNAL", False, 500,
                   "Model configuration error.", cause=err)
    if status and status >= 500:
        return app("LLM_UNAVAILABLE", "DEPENDENCY", True, 503,
                   "The model is unavailable; retrying.", cause=err)
    return unknown("llm", err)
```

## Dialect 4 — OS / network

Tool calls inside `AgentRun` and outbound HTTP everywhere surface socket errors.

```ts
function fromOs(e: NodeJS.ErrnoException): AppError {
  switch (e.code) {
    case "ECONNRESET": case "ECONNREFUSED":
      return app("UPSTREAM_UNAVAILABLE", "DEPENDENCY", true, 503, "A connection failed.");
    case "ETIMEDOUT":
      return app("UPSTREAM_TIMEOUT", "DEPENDENCY", true, 504, "A connection timed out.");
    case "ENOENT":
      return app("FILE_NOT_FOUND", "VALIDATION", false, 404, "The file was not found.");
    default:
      return unknown("os", e);
  }
}
```

## One consumer, four dialects

Because every adapter produced the same shape, the consumers are trivial:

```ts
// Retry engine — dialect-agnostic.
if (err.transient && attempt < maxAttempts) {
  await sleep(err.retryAfterMs ?? backoff(attempt));
  continue;
}

// HTTP mapper — dialect-agnostic.
res.status(err.httpStatus ?? 500).json(problem(err));

// Job boundary — dialect-agnostic.
return err.transient ? { outcome: "retry" } : { outcome: "dead-letter", code: err.code, cause: err.cause };
```

No `switch` on `card_declined`, `SlowDown`, `context_length_exceeded`, or `ECONNRESET` exists
outside the adapters.

## The unknown() helper

Every adapter shares one safe fallback (Ch. 16.14):

```ts
function unknown(source: string, e: any): AppError {
  const status = statusOf(e);
  log.warn({ source, status, err: e }, "unmapped provider error"); // alert-worthy
  return app("PROVIDER_ERROR", "DEPENDENCY", status >= 500, status >= 500 ? 503 : 400,
             "An unexpected provider error occurred.", { provider: source });
}
```

## Key data / numbers

- Stripe types: `card_error` (`402`), `rate_limit_error` (`429`), `api_connection_error`,
  `authentication_error`, `invalid_request_error`.
- S3 codes: `SlowDown` (`503`), `RequestTimeout`, `NoSuchKey` (`404`), `AccessDenied` (`403`).
- LLM: `rate_limit_exceeded` (`429`, transient), `context_length_exceeded` (permanent),
  `invalid_api_key` (config), provider `5xx` (transient).
- OS: `ECONNRESET`/`ECONNREFUSED`/`ETIMEDOUT` transient; `ENOENT` permanent.
- Unknown default: `transient = (status >= 500)`.

## Real-world use case — Acme SaaS

A single Acme workflow charges a card, exports to S3, and runs an LLM summary. Each adapter
normalizes at its edge, so the saga's retry logic is one function checking `transient`. When the
payment team added a second provider, they wrote one adapter and mounted it under the same
`AppError` contract — the saga, HTTP mapper, and job boundary were untouched. The `unknown()` helper
caught a brand-new LLM error code in staging before it ever hit production.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Normalize each dialect at its adapter | Let vendor formats reach consumers |
| Use one shared `AppError` shape | Give each subsystem its own error type |
| Share one safe `unknown()` fallback | Throw inside a translator on unknown codes |
| Preserve `retryAfterMs` from `429` | Drop the server's retry hint |
| Keep `provider` in internal `meta` only | Expose provider names to clients |

## Common mistakes

- **Per-subsystem error shapes** so retry/HTTP logic branches on vendor formats.
- **No `unknown()` branch**, so a new provider code crashes the adapter.
- **Dropping `retryAfterMs`**, turning a `429` into an immediate retry storm.
- **Leaking `provider`/vendor codes** into the public response body.

## Checklist

- [ ] All four dialects normalize into one `AppError` shape.
- [ ] Each adapter owns its vendor mapping end-to-end.
- [ ] A shared `unknown()` handles unmapped codes safely and alerts.
- [ ] `transient` and `retryAfterMs` are always set correctly.
- [ ] Consumers never `switch` on vendor formats.

## Related

- [Postgres SQLSTATE → Domain Error → HTTP Status](./01-postgres-sqlstate-to-domain-to-http.md)
- [Avoiding Overgeneralization and Handling Unknowns](../01-concepts/04-avoiding-overgeneralization-and-unknowns.md)
- [Part X — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
