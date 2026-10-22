# Chapter 21 — Reference

> Part VIII · Chapter 21 · Middleware ordering cheat sheet, exceptions-to-response map, and
> chapter glossary.

## Middleware ordering cheat sheet

```text
requestId            (first: everything logged needs it)
  → sizeGuard        (413: reject before buffering)
  → contentTypeGuard (415: reject before parsing)
  → parse            (400: normalize parser errors)
  → authenticate     (401 + WWW-Authenticate)
  → authorize        (403, or 404 to hide existence)
  → rateLimit        (429 + Retry-After; identity-keyed → after auth)
  → routes
  → notFound         (404 problem for unmatched routes)
  → globalErrorHandler (catch-all: outermost/last, terminal)
```

Framework placement:

| Framework | Catch-all model | Placement |
| --------- | --------------- | --------- |
| Express | Linear; 4-arg error handler | **Last**, after routes |
| Koa | Onion; `try { await next() } catch` | **Outermost (first)** |
| Fastify | `setErrorHandler`, encapsulated | **Root** instance (or per-plugin deliberately) |

Headers-sent flag: `res.headersSent` (Express) · `ctx.headerSent` (Koa) · `reply.sent` (Fastify).

## Exceptions-to-response map

| Failure | Section | Status | Code (example) | Headers |
| ------- | ------- | ------ | -------------- | ------- |
| Unparseable body | 21.2/21.12 | `400` | `MALFORMED_JSON` | — |
| Wrong root type / bad encoding | 21.12 | `400` | `MALFORMED_REQUEST` | — |
| Unsupported media type | 21.13 | `415` | `UNSUPPORTED_MEDIA_TYPE` | `Accept-Post` |
| Oversized body | 21.14 | `413` | `PAYLOAD_TOO_LARGE` | — |
| Oversized headers | — | `431` | `HEADERS_TOO_LARGE` | (HTTP layer) |
| Missing/invalid/expired credential | 21.3 | `401` | `TOKEN_MISSING`/`TOKEN_EXPIRED` | `WWW-Authenticate` |
| IdP outage during auth | 21.3 | `503` | `AUTH_PROVIDER_UNAVAILABLE` | `Retry-After` |
| Authenticated but forbidden | 21.4 | `403` | `INSUFFICIENT_ROLE` | — |
| Cross-tenant access (hiding) | 21.4 | `404` | `RESOURCE_NOT_FOUND` | — |
| Rate/quota exceeded | 21.5 | `429` | `RATE_LIMITED`/`QUOTA_EXCEEDED` | `Retry-After` |
| Rate-limiter store down | 21.5 | `503` | `RATE_LIMITER_UNAVAILABLE` | `Retry-After` |
| Handler deadline exceeded | 21.6 | `503`/`504` | `HANDLER_TIMEOUT` | `Retry-After` |
| Success serialization failure | 21.7 | `500` | `INTERNAL_ERROR` | — |
| Mid-stream failure (SSE) | 21.8/21.11 | `200` + `event: error` | `PROVIDER_*` | — |
| Mid-stream failure (raw stream) | 21.8/21.11 | abort | — | — |
| Write to closed socket | 21.11 | abort | — | — |
| Client aborted | 21.15 | none | — | — |
| Any unhandled/unknown error | 21.18 | `500` | `INTERNAL_ERROR` | — |

## Zone decision table

| Question | Answer | Action |
| -------- | ------ | ------ |
| Has the head been committed? | No | Build problem → send (status + `application/problem+json` + `requestId`) |
| Has the head been committed? | Yes, protocol has in-band errors (SSE) | Emit error frame with `code`, then close |
| Has the head been committed? | Yes, raw byte stream | Abort the connection |
| Has the head been committed? | Yes, already ended | Log only |

## Content-negotiation reminders (Ch. 20 §20.12)

- Errors always: `Content-Type: application/problem+json`.
- `Accept` governs the response representation, not the error shape; do not vary errors by
  `Accept`.
- `Content-Type` (request) drives `415`; `Accept-Post` advertises accepted request types.
- `Vary: Accept` only on responses whose representation varies.

## Timeout ordering

```text
edge/header timeout  ≥  edge/body timeout  >  app handler deadline  >  upstream timeout
```

If inverted, the gateway cuts first and its anonymous `504` replaces your classified envelope.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Global handler | The boundary that catches every error in the request chain |
| Catch-all boundary | The outermost handler guaranteeing a response or a deliberate abort |
| Zone A / B / C | Before handler / in handler / after head committed |
| Head committed | The status line and headers have been sent; status is immutable |
| Swallowing | Catching an error without handling or propagating it |
| Aborted client | Peer closed the connection before the response finished |
| Transmission failure | A write failing after the head is committed |
| In-band error frame | A protocol-level error message inside an otherwise successful stream |

## Signposts

- Compose a chain → [A Complete Middleware Chain](../03-practical-examples/01-a-complete-middleware-chain.md)
- Edge failures → [Handling 413, 415, 400, and Client Aborts](../03-practical-examples/02-handling-413-415-400-and-aborts.md)
- Ordering internals → [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)
- Response-already-started → [The Response-Already-Started Problem](../02-deep-dive/02-response-already-started.md)

## Related

- [Chapter 21 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 20 Reference](../../20-standardized-api-error-responses/05-reference/README.md)
- [Part VIII Index](../../README.md)
