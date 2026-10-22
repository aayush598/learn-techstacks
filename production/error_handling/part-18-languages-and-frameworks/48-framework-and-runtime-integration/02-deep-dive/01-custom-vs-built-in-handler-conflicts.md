# Custom vs Built-in Handler Conflicts

> Part XVIII · Chapter 48 · Sections 48.1–48.4, 48.9–48.12 · _Estimated reading time: 24 min_
> **Prerequisite:** [Framework Hierarchies and Handlers](../01-concepts/01-framework-hierarchies-and-handlers.md), [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)

## In one sentence

**Built-in handlers win by default** — conflicts arise from wrong order, swallowing, or
running after headers have been sent — and they can turn a classified domain error into an
unclassified 500.

## Why this matters in production

In an Express app, a middleware called `next(err)` after `res.json()` did nothing; in
Fastify, a child context overrode the parent's handler incorrectly; in NestJS, a filter threw
another exception creating an infinite loop. Each conflict is subtle and only appears under
real request flows.

## The most common conflicts

### 1. Order of registration (Express)

```ts
// WRONG: error middleware registered before routes
app.use(errorHandler);        // will never catch route errors
app.get('/checkout', handler);
```

```ts
// RIGHT: routes first, error middleware last
app.get('/checkout', handler);
app.use(errorHandler);        // catches errors passed via next(err)
```

If you have multiple error middlewares, they run in registration order. Only the first one that
sends a response should do so.

### 2. Swallowing in middleware

```ts
app.use(async (req, res, next) => {
  try {
    await auth(req);
    next();
  } catch (e) {
    // WRONG: swallowed, next never called with error, request hangs or returns default
    // next(e); missing
  }
});
```

A caught exception with no `next(err)` and no response sent causes the request to hang or
hit the framework's default behavior unpredictably.

### 3. Headers already sent

Once `res.headersSent` is true, you **cannot** change the status code or body. Your error
handler must detect this and delegate to `next(err)` or just log.

```ts
app.use((err, req, res, next) => {
  if (res.headersSent) {
    return next(err); // let the default handler or upstream deal with it
  }
  const appErr = normalize(err);
  const p = policyFor(appErr.code);
  res.status(p.status).json(toProblem(appErr, p, req));
});
```

### 4. Conflicting filters (NestJS)

- Method-scoped `@UseFilters()` runs before controller-scoped, which runs before global.
- If a filter catches an exception and re-throws a different one, the next filter in the
  chain runs.
- If a filter does not re-throw and does not send a response, NestJS falls back to the
  default exception filter.

### 5. Context overrides (Fastify)

Fastify error handlers are inherited down the encapsulation tree. A plugin that calls
`setErrorHandler` will override its parent's handler for routes in that plugin. If you want
to fall back, call `fastify.errorHandler.call(parent, err, req, reply)` or just re-throw.

### 6. Startup vs request errors

If you `throw` during `app.listen()` or module initialization and it's caught by a
request-scoped handler, the process may appear to start incorrectly. **Bootstrap must be
separate from the HTTP server lifecycle.**

```ts
async function bootstrap() {
  const app = await createApp();
  await app.init();        // DI init, DB connect
  await app.listen(3000);  // bind after init
}
bootstrap().catch(err => {
  logger.fatal({ err }, 'startup_failed');
  process.exit(1);
});
```

### 7. Shutdown conflicts

During `SIGTERM`, if your error handler tries to write to a closed socket or a drained
connection pool, it will throw again. During shutdown, **log only, don't send HTTP
responses**.

## Conflict matrix

| Conflict | Framework | Symptom | Fix |
| -------- | --------- | ------- | --- |
| Wrong order | Express | Errors return framework defaults or hang | Register error middleware last |
| Swallowed | Express/NestJS | Request hangs, no response | Always `next(err)` or re-throw |
| Headers sent | Express | `Can't set headers after they are sent` | Check `res.headersSent`, delegate to `next(err)` |
| Filter loop | NestJS | Stack overflow, infinite recursion | Don't re-throw unless you know a higher filter will handle; avoid throwing from filters |
| Context override | Fastify | Child routes use wrong error shape | Be explicit about inheritance; test plugin boundaries |
| Startup routed to HTTP handler | All | Misleading 500s at boot; health checks fail oddly | Fail-fast in `bootstrap().catch()` with exit code |
| Shutdown crash | All | Process won't exit cleanly | Catch all errors in shutdown handlers; use timeouts |

## How to debug conflicts

1. **Trace the chain:** Log which middleware/filter handled the error (name/id).
2. **Check order:** Print the middleware stack at startup in dev.
3. **Test headers-sent:** Simulate streaming responses where an error occurs mid-stream.
4. **Test startup:** Kill the DB and observe the exit code and first log line.
5. **Test shutdown:** Send `SIGTERM` mid-request and mid-job.

## Key data / numbers

- Express requires **exactly 4 arguments** for error middleware — using rest params can
  mask this.
- NestJS filters that don't send a response and don't re-throw will result in a fallback
  to the base filter (often returning `500`).
- Fastify's default error handler sets status from `error.statusCode` if present, else `500`.
- On shutdown, use a **drain timeout** (e.g. 10s for HTTP, 30s for jobs) before forcing exit.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Document middleware/filter order in code comments | Rely on "it works" without testing order |
| Handle `res.headersSent` in Express error middleware | Call `res.json()` unconditionally |
| Fail fast on bootstrap with `process.exit(1)` | Let startup exceptions bubble to the HTTP handler |
| Make shutdown handlers idempotent and time-limited | Throw exceptions during `SIGTERM` handling |
| Test filter precedence in NestJS | Create circular filter chains |

## Checklist

- [ ] Is the error handler registered in the correct position?
- [ ] Are all middleware that catch exceptions re-throwing or calling `next(err)`?
- [ ] Does the handler guard against `headersSent`?
- [ ] Are bootstrap failures separate from request handling?
- [ ] Is graceful shutdown time-bound and exception-safe?

## Related

- [Framework Hierarchies and Handlers](../01-concepts/01-framework-hierarchies-and-handlers.md)
- [Framework-Independent Policy and Adapters](../01-concepts/03-framework-independent-policy-and-adapters.md)
- [Express, Fastify, and NestJS Adapters](../03-practical-examples/01-express-fastify-and-nestjs-adapters.md)
- [Chapter 11 — The Error Lifecycle](../../../part-04-architecture/11-the-error-lifecycle/README.md)
