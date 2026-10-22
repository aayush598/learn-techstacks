# Chapter 21 — API Boundary and Middleware Error Handling

> Part VIII · _Estimated reading time: 70–95 min_
> **Prerequisite:** [HTTP Error Semantics (Ch. 19)](../19-http-error-semantics/README.md), [Standardized API Error Responses (Ch. 20)](../20-standardized-api-error-responses/README.md)

## One-sentence summary

The **middleware chain is your error boundary** — if parsing, auth, rate limits, handlers, and
serialization each throw without a unified catch-all, the contract from Ch. 20 is never
guaranteed; middleware ordering and a hardened catch-all are correctness properties, not style
preferences.

## Why this chapter matters

A perfect status selection (Ch. 19) and a perfect envelope (Ch. 20) fail the moment an
unhandled exception escapes at the wrong time. If it escapes **before** the handler, your
framework may return HTML. If it escapes **after headers are sent**, you cannot change the
status code — you can only log and close the connection. If the catch-all re-throws or
serializes raw `Error` objects, you leak internals and violate the envelope contract. This
chapter maps the chain, fixes ordering, handles the "headers already sent" class of failures,
and builds a catch-all boundary that produces a valid Problem Details response on every path.

## Chapter map

The chapter has 18 sections grouped into ten files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-global-handlers-and-the-request-boundary.md`](./01-concepts/01-global-handlers-and-the-request-boundary.md) | 21.1, 21.9, 21.10, 21.18 | Global handlers, the three failure zones, errors before the handler, headers-already-sent, the catch-all boundary |
| [`01-concepts/02-parsing-and-malformed-requests.md`](./01-concepts/02-parsing-and-malformed-requests.md) | 21.2, 21.12, 21.13, 21.14 | Parsing failures, malformed requests, unsupported content types, oversized payloads (`400`/`413`/`415`/`431`) |
| [`01-concepts/03-auth-authz-and-rate-limit-middleware.md`](./01-concepts/03-auth-authz-and-rate-limit-middleware.md) | 21.3, 21.4, 21.5 | Auth/authz classification and ordering, rate limiting position, `401`/`403`/`429` with the required headers |
| [`01-concepts/04-timeouts-streaming-and-connection-lifecycle.md`](./01-concepts/04-timeouts-streaming-and-connection-lifecycle.md) | 21.6, 21.7, 21.8, 21.11, 21.15 | Timeouts, serialization, streaming, transmission errors, aborted client connections |
| [`01-concepts/05-ordering-and-swallowing.md`](./01-concepts/05-ordering-and-swallowing.md) | 21.16, 21.17 | Middleware ordering as a correctness property; the swallowing anti-pattern |
| [`02-deep-dive/01-middleware-ordering-mechanics.md`](./02-deep-dive/01-middleware-ordering-mechanics.md) | 21.16 | Express/Koa/Fastify ordering models, catch-all placement, and the ordering matrix |
| [`02-deep-dive/02-response-already-started.md`](./02-deep-dive/02-response-already-started.md) | 21.10, 21.11 | The commit boundary, detection per framework, and log-and-abort recovery |
| [`03-practical-examples/01-a-complete-middleware-chain.md`](./03-practical-examples/01-a-complete-middleware-chain.md) | 21.1–21.18 applied | A full TypeScript chain producing Problem Details on every path |
| [`03-practical-examples/02-handling-413-415-400-and-aborts.md`](./03-practical-examples/02-handling-413-415-400-and-aborts.md) | 21.12–21.15 applied | `413`/`415`/`400` handling and client-abort cancellation |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Ordering cheat sheet, exceptions-to-response map, and chapter glossary |

## Learning objectives

- Design a **global error boundary** that catches every thrown error and returns a valid Problem
  Details document (Ch. 20), never HTML or raw stack traces.
- Place middleware in the correct order: parsing/size checks before authz that depends on body,
  auth before rate limits keyed to identity, rate limits before expensive handlers, and the
  catch-all **outermost**.
- Handle the "headers already sent" case: detect it, **never** attempt to rewrite the status/body,
  log with `requestId`, and abort/close cleanly.
- Classify parsing failures, unsupported content types, oversized payloads, aborted connections,
  and mid-stream transmission failures into correct status codes and safe envelopes.
- Prevent middleware from **swallowing** errors; ensure every error path is either translated to a
  problem or propagated to the catch-all boundary.

## Key takeaways

1. **The catch-all boundary is the last line of defense.** If any path can throw outside it, the
   contract is not guaranteed. Make it outermost.
2. **Ordering is correctness.** Rate limiting per-identity must run after auth (or you throttle
   the wrong key); parsing must run before schema-dependent authz; size checks before buffering.
3. **After headers are sent, you cannot change the response.** This is non-negotiable: on write
   failure mid-stream, log and close — do not attempt to send a second JSON error body.
4. **Classify early.** `413`, `415`, `400` (parse) are caught at the edge middleware with safe
   Problem Details, not as unhandled exceptions.
5. **Never swallow.** A middleware that `catch { /* ignore */ }` converts observable failures into
   silent corruption. Either translate and respond, or re-throw to the boundary.

## Exercises

1. Draw your middleware chain and mark: (a) where each of 21.2–21.15 executes, (b) the catch-all
   position, (c) the "headers sent" detection point.
2. Write a test that forces a serialization error after headers are sent and asserts only logging
   occurs (no attempt to write a second body).
3. Trace `WebhookIngest`'s signature verification failure through the chain: which middleware
   catches it, which status, and why.
4. For a streaming `AgentRun` response, list three transmission failure modes and the exact
   boundary behavior for each.

## Related

- [HTTP Error Semantics (Ch. 19)](../19-http-error-semantics/README.md)
- [Standardized API Error Responses (Ch. 20)](../20-standardized-api-error-responses/README.md)
- [Error Boundaries (Part VI, Ch. 15)](../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Glossary](../../GLOSSARY.md)
