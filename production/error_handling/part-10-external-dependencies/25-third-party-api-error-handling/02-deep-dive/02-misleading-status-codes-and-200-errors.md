# Misleading Status Codes and 200 Errors

> Part X · Chapter 25 · Section 25.2, 25.16 · _Estimated reading time: 14 min_

## In one sentence

**Some providers return 200 OK with an error body or use non-standard status codes** — you must detect these and classify them as upstream failures, not treat them as success.

## Why this matters in production

If **Checkout** calls a provider and gets `200 OK` with `{ "error": { "message": "card declined" } }`, blindly checking `res.ok` would treat it as success and proceed to mark an order as paid. That's catastrophic. Similarly, some gateways return `422` for things that are really "unavailable" or use `400` to hide rate limits. You cannot trust status codes alone.

## Core concept

| Pattern | Example | Classification |
| ------- | ------- | -------------- |
| **200 with error body** | `200 OK` + `{error:{type:'card_error'}}` | Upstream failure (business/decline or error) |
| **4xx for transient issues** | `409` used for throttling, or `400` for rate limit | Must inspect body/headers |
| **5xx vs gateway errors** | `502/503/504` from LB/proxy | Often network/upstream unavailability |
| **Misleading semantics** | Provider uses `422` where you expect `400` | Translate to internal category, map to correct HTTP later |

## How it works

### Detection
1. **Check body even if ok** — if response has error structure, treat as failure.
2. **Check headers** — `Retry-After`, rate limit headers may indicate throttling regardless of status.
3. **Inspect content-type** — HTML error pages often come with 4xx/5xx.
4. **Distinguish gateway vs origin** — `502` from LB may mean origin timed out.

### Classification rules
- **If body indicates error** → upstream failure, classify by payload.
- **If status is 429** → rate limit (check Retry-After).
- **If status 502/503/504** → often retryable transport/gateway issues (if idempotent).
- **If status 4xx and body is business error** → usually non-retryable.

## Worked example

```ts
async function handleResponse(res: Response) {
  const parsed = await parseUpstream(res); // from earlier
  // 200 with error body
  if (parsed.kind === "json" && res.ok) {
    const body: any = parsed.body;
    if (body.error || body.errors) {
      // It's a failure despite 200
      return classifyProviderError({ status: res.status, body, headers: res.headers });
    }
    // true success
    return { ok: true, data: body };
  }
  // non-ok or non-json
  return classifyProviderError({ status: res.status, body: parsed.body, headers: res.headers });
}
```

**Key data:**
- **gRPC over HTTP/2**: Status codes differ; `grpc-status` header matters.
- **Stripe**: Rarely returns 200 with error, but other providers do.
- **LB errors**: `503` may be from gateway with no origin body.

## Real-world use case

**WebhookIngest processing provider callbacks:** A provider posts to your webhook endpoint but the call to validate comes from your side? Or more directly, **Checkout** calling a third-party PSP that returns `200 OK` with `{ "status": "DECLINED", "reason": "insufficient_funds" }`. Without body inspection, you would capture payment and create a paid order. Correct classification treats this as `UPSTREAM_DECLINED` (non-retryable) and leaves order unpaid.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Trust status only** | Simple | Catastrophic for 200-with-error | **Never** |
| **Always inspect body on non-ok** | Correct | Some bodies large | **Recommended** |
| **Inspect body on ok if schema says error possible** | Catches 200-with-error | Need to know per-endpoint | **Recommended** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Inspect response body even for `res.ok` | Treat `200 OK` as success unconditionally |
| Check for error structures (`error`, `errors`, `status: 'ERROR'`) | Assume provider follows REST semantics strictly |
| Distinguish LB errors from origin errors | Conflate `502` from gateway with origin 500 |
| Translate before acting on success/failure | Let misleading status drive business logic |

## Common mistakes

- **200-with-error blindness:** Biggest source of incorrect "success".
- **Trusting gateway HTML:** Treating HTML as JSON.
- **Status code translation errors:** Mapping everything to same internal category.
- **Not handling content negotiation:** XML vs JSON error shapes.

## Checklist

- [ ] Response handler inspects body for error indicators on both ok and non-ok.
- [ ] 200-with-error classified as failure.
- [ ] LB/gateway errors (502/503/504) classified separately.
- [ ] Parser handles non-JSON error pages.
- [ ] Tests cover 200-with-error cases per vendor.

## Related

- [Provider Error Translation Mechanics](./01-provider-error-translation-mechanics.md)
- [Malformed Responses, Versioning, and Degradation](../01-concepts/03-malformed-responses-versioning-degradation.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../26-network-and-distributed-communication-errors/README.md)
- [Glossary](../../../GLOSSARY.md)
