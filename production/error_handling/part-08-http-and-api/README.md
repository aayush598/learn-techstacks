# Part VIII — HTTP and API Error Handling

> **Chapters 19–21.** Every failure inside your process becomes real to the outside world only
> when it crosses the HTTP boundary. This part defines the three things that boundary must get
> right: **which status code tells the truth** (Ch. 19), **which response body the client can
> parse and act on** (Ch. 20), and **where in the middleware chain each failure is caught,
> translated, and serialized** (Ch. 21). Get these wrong and your taxonomy, error model, and
> boundaries from Parts II–VI never reach the client intact.

## Learning objectives

By the end of Part VIII you will be able to:

1. Select the **correct HTTP status code** for any failure using one consistent, documented
   rule set — never "whatever the handler happened to return."
2. Distinguish the fine-grained client errors (`400` vs `422`, `401` vs `403`, `404` vs `410`,
   `409` vs `422`) and defend each choice against your team and your API consumers.
3. Design an **error envelope** on RFC 9457 Problem Details that carries your internal error
   codes, field-level validation details, and request IDs without leaking stack traces, SQL, or
   infrastructure topology.
4. Place error handling correctly in the **middleware chain**: what runs before the handler,
   what runs after headers are already sent, what happens on aborted connections and mid-stream
   failures, and why ordering is a correctness property, not a style preference.
5. Build a **catch-all boundary** that is guaranteed to produce a valid response for any
   failure — including failures in serialization, in other middleware, and after the response
   head is on the wire.
6. Keep error contracts **stable and honest** as your API versions, your SDKs, and your
   third-party integrations evolve.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 19 | [HTTP Error Semantics](./19-http-error-semantics/README.md) | Status-code families, the full 4xx/5xx selection table, 400-vs-422, 401-vs-403, Retry-After, never returning 200 for failures, never exposing internals |
| 20 | [Standardized API Error Responses](./20-standardized-api-error-responses/README.md) | RFC 9457 Problem Details, error envelope, type/title/detail/instance, app codes, field details, request IDs, versioning, SDK and third-party contracts |
| 21 | [API Boundary and Middleware Error Handling](./21-api-boundary-and-middleware-error-handling/README.md) | Global handlers, parsing/auth/rate-limit middleware, timeouts, streaming, headers-already-sent, aborted clients, ordering, swallowing, catch-all boundary |

## How the three chapters fit together

```text
   Chapter 19 ── the SEMANTICS view ──▶  "what status code means what?"
   Chapter 20 ── the CONTRACT view ───▶  "what does the body say?"
   Chapter 21 ── the MECHANICS view ──▶  "which code produces that response, and when?"
```

Chapters 19 and 20 define the *contract*: status + headers + body. Chapter 21 defines the
*mechanism*: the middleware chain that must deliver that contract on every path, including the
ugly ones (malformed JSON, aborted sockets, errors thrown while writing the error itself). A
perfect contract with no catch-all boundary produces HTML error pages from your framework; a
perfect boundary with sloppy status selection produces a beautifully formatted wrong answer.

## The recurring cast in Part VIII

| Cast member | API surface exercised |
| ----------- | --------------------- |
| **Acme SaaS** | Multi-tenant REST API (`/api/v1/...`): projects, members, uploads — validation, tenancy, quota errors |
| **Checkout** | `POST /api/v1/checkout` — idempotency, payment conflicts (`409`), provider failures (`503` + `Retry-After`) |
| **ExportJob** | `POST /api/v1/exports`, `GET /api/v1/exports/{id}` — `202` + job states, `410` for expired results |
| **WebhookIngest** | `POST /api/v1/webhooks/stripe` — signature failures (`400`), fast `200` acks, replay safety |
| **AgentRun** | `POST /api/v1/agent/runs` — long-running, streaming responses, mid-stream failures, rate limits |

## Key takeaways

- **A status code is a machine contract, not a vibe.** Clients branch on it; SDKs retry based
  on it; proxies and load balancers cache on it. Pick it from a documented table, not ad hoc.
- **`200` with an error body is a lie** the client cannot act on. Legitimate exceptions are
  narrow (207-style multi-status semantics, deliberately polled "operation result" endpoints)
  and must be documented as such.
- **RFC 9457 Problem Details is the default answer** for error bodies in modern HTTP APIs:
  one media type (`application/problem+json`), five standard members, unlimited extensions.
- **Middleware order is part of the error contract.** Parsing must precede authz decisions that
  depend on the body; the catch-all must be outermost; rate limiting should run before
  expensive authentication when the limit is per-IP.
- **After headers are sent you cannot change the status code.** Design for that: log, abort
  the connection, and never attempt a second write of a JSON error body mid-stream.
- **Consistency beats cleverness.** One selection table, one envelope, one boundary — the same
  for `Checkout` and `AgentRun`, today and in eighteen months.

## Related

- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md) (the boundary theory this part applies to HTTP)
- [Part IV — Error-Handling Architecture](../part-04-architecture/README.md) (layer responsibilities the middleware chain implements)
- [Glossary](../GLOSSARY.md)
