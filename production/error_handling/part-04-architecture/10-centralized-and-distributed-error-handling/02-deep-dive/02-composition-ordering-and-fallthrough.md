# Composition, Ordering, and Fallthrough

> Part IV · Chapter 10 · Sections 10.5–10.7 · _Estimated reading time: 19 min_
> **Prerequisite:** [The Machinery of Centralized Handling](../01-concepts/02-the-machinery-of-centralized-handling.md)

## In one sentence

Middleware, interceptors, and decorators **compose in a specific order**, and an error's final
response is decided by the **first layer that both catches it and writes the body** — so ordering
mistakes, not missing handlers, are the usual cause of wrong statuses and corrupted bodies.

## Why this matters in production

The error path is exercised under load, at 3 a.m., by the failures you least control. Ordering
bugs surface then:

- Rate-limit middleware runs **after** the handler → a flooded endpoint overloads the app before
  the limiter ever sees the requests.
- The serializer runs **after** headers were already sent → Node raises
  `ERR_HTTP_HEADERS_SENT`, the client gets a truncated body, and the original error is masked by
  the serialization error.
- Two layers both "fall through" on an unknown error → the default framework handler renders
  `{"message":"Internal Server Error"}` in a *different* shape, breaking clients that parse your
  envelope.
- A decorator wraps in the wrong order → retries run **outside** the logging wrapper and the
  retried attempts are invisible.

## Core concept — the composition model

Think of request handling as nested wrappers (Russian dolls). The **outermost** layer that
successfully writes the response wins; everything inside must then stay silent.

```text
 ┌─ rate-limit ──────────────────────────────────────────────┐
 │ ┌─ auth ────────────────────────────────────────────────┐  │
 │ │ ┌─ request-id / correlation ───────────────────────┐  │  │
 │ │ │ ┌─ handler (controller → app) ────────────────┐  │  │  │
 │ │ │ │                                              │  │  │  │
 │ │ │ │   thrown AppError travels OUTWARD ───────────┼──┼──┼──▶ first
 │ │ │ └──────────────────────────────────────────────┘  │  │  │   catcher
 │ │ │   interceptor: normalize thrown/returned          │  │  │   writes
 │ │ └───────────────────────────────────────────────────┘  │  │   body
 │ │   auth failure: written HERE, inner layers never run    │  │
 │ └────────────────────────────────────────────────────────┘  │
 │   rate limit: written HERE, nothing inner runs              │
 └─────────────────────────────────────────────────────────────┘
        error filter / serializer (outermost on the ERROR path)
```

Ordering rules that follow:

1. **Outermost → innermost for preconditions:** request ID → rate limit → auth → parse → handler.
   Each precondition may terminate before the next runs (fail-fast, Chapter 2).
2. **Inward for normalization:** interceptors/adapters normalize as close to the handler as
   possible so outer layers only see `AppError`.
3. **Outward for errors:** the error travels out; the **first** layer that recognizes it writes
   the response; every layer must check `headersSent` (or framework equivalent) before writing.
4. **Exactly one body-writer.** In practice: the error filter. Middleware may write only for
   failures it *caused* (auth → 401) and must not re-enter the filter's path afterward.

## How it works — the hazards in code

### Double serialization after headers are sent

```ts
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  // ❌ missing guard: a streaming handler already wrote 200 + partial body
  res.status(500).json(toProblem(normalize(err), req.id));   // ERR_HTTP_HEADERS_SENT

  // ✅ correct
  if (res.headersSent) return next(err);   // hand off to process-level handling (Ch. 9, 9.12)
  const e = normalize(err);
  res.status(STATUS[e.code] ?? 500).json(toProblem(e, req.id));
});
```

Once headers are on the wire, the status is immutable; the honest options are aborting the
connection or letting the framework finish the stream — both are terminal, and both must be
logged with the correlation ID (Chapter 21 covers streaming edge cases).

### Order-dependent fallthrough

```ts
// ❌ BAD ORDER — auth after handler means unauthenticated requests hit business logic
app.use(handler); app.use(auth);

// ✅ preconditions outermost
app.use(requestId); app.use(rateLimit); app.use(auth); app.use(routes);
app.use(errorFilter);   // registered LAST; Express finds it via 4-arg signature
```

### Decorator wrapping order

```ts
// ❌ retry OUTSIDE logging: retried attempts produce no logs
@Retryable({ attempts: 3 })
@AuditLog()
async charge() { ... }

// ✅ logging OUTSIDE retry: every attempt is audited; retry policy stays declarative
@AuditLog()
@Retryable({ attempts: 3 })
async charge() { ... }
```

Order reads bottom-up in most decorator implementations: the decorator closest to the method
wraps first. Write the intent ("what must see every attempt?") before writing the stack.

## Composition checklist per layer

| Layer | Must | Must never |
| ----- | ---- | ---------- |
| rate limit | write `429` + `Retry-After` itself | call the handler after writing |
| auth | write `401`/`403` itself | leak *which* check failed in the message |
| parse/validation | write `400`/`422` with field errors | enter the transaction |
| interceptor | normalize shapes; attach deadline/ID | retry, compensate, or write bodies |
| error filter | serialize **once**, after `headersSent` check | branch on business context |
| decorator (central) | one concern (serialize/audit) | hide control flow side effects |

## Key data / numbers

- Express error middleware: **4 parameters** `(err, req, res, next)`; registered **after**
  routes; order among multiple error middlewares is registration order (first match wins).
- Node: a second write raises `ERR_HTTP_HEADERS_SENT`; once `writeHead` ran, status is fixed.
- NestJS order of execution on the way in: **middleware → guards → interceptors (before) →
  pipes → handler**; on the way out: **interceptors (after) → exception filters**.
- FastAPI/Starlette: exception handlers run **outside** dependency teardown failures only if the
  exception propagates; response middleware runs after the handler — do not write twice.
- Recommendation: cap the stack at **one** error-writing layer plus at most **one** precondition
  layer per concern (auth, limit, parse).

## Real-world use case — Acme SaaS export download

Acme streamed export CSVs: the handler wrote `200` and streamed rows; a mid-stream S3 failure
threw; the error filter tried `res.status(500).json(...)` → `ERR_HTTP_HEADERS_SENT` →
the response ended **mid-row with HTTP 200**, and the customer's CSV looked complete but was
truncated. Files with 60 % of rows passed as "successful."

Fix: (1) the filter checked `headersSent` and aborted the stream (`res.destroy()`), which the
client sees as a broken transfer instead of a fake success; (2) the job-side record stayed the
source of truth for completeness; (3) downloads moved to pre-signed URLs so no application stream
sat on the error path at all. The "silent truncated success" class of bug disappeared.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single body-writing filter + strict ordering (recommended) | Predictable; one place to test | Discipline required for streaming routes | Default |
| Each middleware writes its own errors | Locally simple | Inconsistent envelopes; double-write risk | Only for precondition layers (auth/limit) |
| Catch in every layer and serialize everywhere | Feels safe | Guaranteed duplication | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register preconditions outermost, filter last | Register the error filter before routes |
| Check `headersSent` before serializing | Write a response after streaming began |
| Normalize close to the handler | Let raw framework exceptions reach outer layers |
| Make decorator order an explicit review item | Stack decorators without stating wrap order |

## Common mistakes

- **Middleware calling `next(err)` after writing a body** — the filter then double-writes; write
  *or* forward, never both.
- **Assuming all frameworks order the same** — NestJS, Express, and FastAPI differ; document
  *your* stack's order in the chapter reference style above.
- **Serialization errors masking the original** — wrap the serializer itself in its own
  try/catch that falls back to a hard-coded minimal body plus correlation ID.

## Checklist

- [ ] Your stack's order (preconditions → handler → filter) is written down.
- [ ] Exactly one layer writes error bodies for handled errors.
- [ ] `headersSent`/equivalent guards exist on every writer.
- [ ] Streaming routes define abort semantics for mid-stream failures.
- [ ] Decorator wrap order is tested by a log/retry assertion.

## Related

- [The Machinery of Centralized Handling](../01-concepts/02-the-machinery-of-centralized-handling.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Chapter 9 — Async Layers and Process Boundaries](../../09-layered-error-handling-architecture/02-deep-dive/02-async-layers-workers-and-scheduled-tasks.md)
