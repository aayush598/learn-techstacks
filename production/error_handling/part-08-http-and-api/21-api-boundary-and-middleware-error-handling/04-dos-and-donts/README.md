# Chapter 21 — Do's and Don'ts

> Part VIII · Chapter 21 · All sections

A condensed rule set for the API boundary and middleware chain. Use it as a review checklist for
any PR that adds or reorders middleware, touches a global handler, or changes a streaming
endpoint.

## The global boundary

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register the catch-all outermost/last (framework-appropriate) | Let the framework default render errors |
| Check `headersSent`/`headerSent`/`sent` before responding | Attempt any response after the head is committed |
| Handle unknown and non-`Error` throws | Assume `err` is always an `Error` |
| Map framework/parser/router errors to registry codes | Expose `SyntaxError`/`PayloadTooLargeError` text |
| Set `requestId` once; echo it in body and `X-Request-Id` | Generate a new id inside the catch-all |
| Log full cause server-side; send the projection | Serialize the caught `Error` |

## Ordering (21.16)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Order by real dependencies: id → size → type → parse → auth → authz → limit | Copy an ordering that "looks right" |
| Key rate limits on identity after authentication | Key identity limits on IP before auth |
| Run body-dependent authz after parsing | Authorize against unparsed data |
| Keep the catch-all outermost for the framework model | Place an Express error handler before routes |
| Generate `requestId` before anything logs | Emit errors with no correlation handle |

## Swallowing (21.17)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Log and meter best-effort failures | Use empty `catch {}` |
| Propagate side effects the client assumes succeeded | Return `200` after a failed enqueue |
| Distinguish "unavailable" from "empty" | Default a failed dependency read to 0/false |
| Suppress a cleanup error only alongside the primary error | Hide a cleanup failure entirely |
| Enable `no-empty-catch`/`no-empty` lints | Treat a lint-disabled catch as "handled" |

## Parsing, types, size, and aborts

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reject on `Content-Length`, then enforce a counted cap | Trust `Content-Length` alone |
| Return `415` for missing/unsupported `Content-Type` | Coerce `text/plain` into JSON |
| Normalize parser errors to `400` `MALFORMED_JSON` | Echo parser offsets/input |
| Keep `400` (syntax) vs `422` (semantic) distinct | Collapse them into one code |
| Align gateway and app limits (gateway ≥ app) | Let a proxy page answer oversized requests |
| Cancel downstream work on client abort | Keep spending tokens/rows after the client left |
| Log aborts at `info`, transmission failures at `error` | Alert on normal navigations-away |

## Timeouts, streaming, and lifecycle

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set handler deadlines shorter than edge timeouts | Let the gateway `504` erase your envelope |
| Pre-flight auth/existence before streaming | Commit `200` then find a `403`-class problem |
| Serialize fully before the head when feasible | Stream a success body that can still throw |
| Define an SSE `event: error` schema | Invent ad hoc mid-stream error formats |
| Abort raw byte streams on mid-stream failure | Append an error object to a partial body |
| Release resources in `finally` on abort | Hold transactions/streams after the client left |

## Anti-patterns

1. **The HTML Boundary** — framework defaults render errors because the catch-all is missing or
   misplaced.
2. **The Second Write** — attempting a problem document after the head is committed
   (`ERR_HTTP_HEADERS_SENT`).
3. **The Middleware Oracle** — middleware answers errors itself, drifting from the envelope.
4. **The Wrong Key** — identity rate limit placed before authentication.
5. **The Silent Swallow** — `catch {}` around a side effect the client assumes succeeded.
6. **The Parser Soapbox** — echoing `SyntaxError` offsets and input fragments.
7. **The False 500** — counting a client abort or a transmission failure as a server error.
8. **The Uncovered Route** — routes registered after the Express error handler.

## Checklist

- [ ] Catch-all is outermost/last and covers parser, auth, and routes.
- [ ] `headersSent` is checked; Zone C logs and aborts.
- [ ] Order matches the documented dependency chain.
- [ ] No empty or default-returning catch remains.
- [ ] `413`/`415`/`400` are edge verdicts in the envelope; gateway limits aligned.
- [ ] Streaming endpoints document and test their mid-stream failure behavior.
- [ ] Golden-set contract fixtures run against the chain.

## Related

- [Chapter 21 Reference](../05-reference/README.md)
- [Global Handlers and the Request Boundary](../01-concepts/01-global-handlers-and-the-request-boundary.md)
- [Do's and Don'ts (Ch. 20)](../../20-standardized-api-error-responses/04-dos-and-donts/README.md)
