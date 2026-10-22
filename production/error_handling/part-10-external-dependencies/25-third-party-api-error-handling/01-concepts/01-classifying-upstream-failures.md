# Classifying Upstream Failures

> Part X · Chapter 25 · Sections 25.1, 25.2, 25.3, 25.8, 25.9 · _Estimated reading time: 16 min_

## In one sentence

**Classify third-party failures by origin** (HTTP semantics, provider payload shape, timeouts, connectivity) because each class implies a different retry/recoverability decision for **Acme SaaS**.

## Why this matters in production

When **Checkout** calls **Stripe**, a `400` from the provider may mean "your request is invalid" (not retryable), while a network `ECONNRESET` means "transport failed" (potentially retryable if idempotent). Treating them the same causes either retry storms or never-retried outages. Precise classification is the input to translation at the integration boundary.

## Core concept

Upstream failures fall into three broad origins:

1. **HTTP-layer failures** — status codes, headers (`Retry-After`, `X-RateLimit-*`), and gateway responses.
2. **Provider-payload failures** — error objects inside the body (often when status is 4xx/5xx or even `200 OK`).
3. **Transport/connectivity failures** — DNS, TCP/TLS, connect/read/write timeouts, connection pools.

Each must be classified before deciding policy.

## How it works (mechanics)

| Origin | Examples | Typical recoverability | Notes |
| ------ | -------- | ----------------------- | -----|
| **HTTP errors** | `400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`, `502`, `503`, `504` | Mixed — see per-code | Semantics vary by provider; don't assume RFC meaning alone. |
| **Provider payloads** | `error.type`, `error.code`, `error.param`, `decline_code` (Stripe-like) | Varies | Often more specific than status code. Must be parsed. |
| **Timeouts** | Connect/read/write timeouts | Often retryable *if idempotent* | Ambiguous if after sending a non-idempotent body (see Chapter 26). |
| **Connection failures** | `ECONNREFUSED`, `ECONNRESET`, DNS failure | Often retryable *if idempotent* | Usually transport-level; classify separately from HTTP. |

## Worked example

Consider **Checkout** creating a payment intent. Three different failures require different actions:

```ts
// Classify failures before translating
type UpstreamClass =
  | { kind: "http"; status: number; headers: Headers }
  | { kind: "provider_payload"; status?: number; body: any }
  | { kind: "network"; code: string; phase: "connect" | "write" | "read" };

function classify(resOrErr: any): UpstreamClass {
  if (resOrErr instanceof NetworkError) {
    return { kind: "network", code: resOrErr.code, phase: resOrErr.phase };
  }
  // http response
  if (resOrErr.status) {
    // some providers put error in body even for 4xx/5xx
    return { kind: "http", status: resOrErr.status, headers: resOrErr.headers };
  }
  return { kind: "provider_payload", body: resOrErr };
}
```

**Key data:**
- **HTTP:** `429 Too Many Requests` often includes `Retry-After` (seconds or HTTP-date). `502/503/504` are common gateway failures.
- **gRPC:** `UNAVAILABLE`, `DEADLINE_EXCEEDED` map to transport/upstream unavailability/timeouts.
- **Network:** `ECONNREFUSED`, `ECONNRESET`, `ETIMEDOUT` are OS-level signals (see Chapter 26).

## Real-world use case

**Acme SaaS — Checkout calling Stripe:** A `card_declined` comes back as HTTP `402` with provider payload `{error:{type:'card_error', code:'card_declined'}}`. This is a **business/decline** error — **not retryable** and should surface a user-actionable message. Meanwhile, `api_connection_error` (network) during an idempotent `POST` to create a charge may be **retryable** with backoff. Classification prevents applying the wrong policy.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Classify by HTTP status only** | Simple | Misses provider payload nuances; misclassifies 200-with-error | Only for trivial, well-behaved APIs |
| **Classify by provider payload first** | Accurate, vendor-specific details available | More parsing; need per-vendor mappers | **Recommended** at integration boundary |
| **Classify by origin (http/payload/network)** | Clean separation, reusable | Slightly more code | **Recommended** as the classification layer before translation |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Parse provider payload even if status is 4xx/5xx | Assume status code alone defines retryability |
| Treat network errors separately from HTTP responses | Call network errors "HTTP 500" internally |
| Check for `Retry-After` on 429/503 | Retry blindly without respecting provider hints |
| Preserve original status/code for translation | Leak raw provider types into domain |

## Common mistakes

- **Status-code absolutism:** Treating all 5xx as retryable and all 4xx as non-retryable — some 4xx (`409` conflict in certain idempotent contexts) need care; some 5xx may be due to bad request shaped by gateway.
- **Ignoring 200-with-error:** Some providers return 200 with `{error:...}` — must detect and classify as upstream failure.
- **Conflating phases:** Connect timeout vs read timeout have different ambiguity implications (see Chapter 26).

## Checklist

- [ ] Every upstream call classifies into `http` | `provider_payload` | `network`.
- [ ] Provider payload parser exists per vendor at the adapter boundary.
- [ ] `Retry-After` and rate-limit headers are captured.
- [ ] Network errors carry `code` and `phase` (connect/write/read).
- [ ] Classification happens before any retry/translation logic.

## Related

- [Auth, Rate Limits, Quotas, and Billing](./02-auth-rate-limits-quotas-and-billing.md)
- [Malformed Responses, Versioning, and Degradation](./03-malformed-responses-versioning-degradation.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../26-network-and-distributed-communication-errors/README.md)
- [Glossary](../../../GLOSSARY.md)
