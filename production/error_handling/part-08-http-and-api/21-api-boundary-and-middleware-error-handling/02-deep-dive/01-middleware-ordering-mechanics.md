# Middleware Ordering Mechanics

> Part VIII · Chapter 21 · Section 21.16 · _Estimated reading time: 19 min_
> **Prerequisite:** [Ordering and Swallowing](../01-concepts/05-ordering-and-swallowing.md)

## In one sentence

Frameworks expose three different mental models for middleware order — **linear registration**
(Express), the **onion/around** model (Koa), and **encapsulated plugin** scoping (Fastify) — and
each decides where the catch-all must live and which layers it can actually see.

## Why this matters in production

"Register the catch-all last" is a rule that is right for Express, subtly wrong for Koa (where it
must be *outermost*, not merely last), and different again for Fastify (where error handling is
centralized and plugin encapsulation changes what a hook sees). Copying an ordering pattern from
one framework into another is a common source of unhandled errors that only appear in production,
under specific thrown paths. This deep-dive makes the mechanics explicit so the order you write is
the order that runs — regardless of runtime.

## Core concept — three models

```text
EXPRESS (linear)              KOA (onion)                 FASTIFY (encapsulated)
 m1 → m2 → handler             m1                          plugin A ─┤ routes A
   errors flow back to           → m2                       plugin B ─┤ routes B
   error handlers registered        → handler               root     ─┤ hooks, error handler
   AFTER the failing layer              ← m2
                                 ← m1 (try/catch wraps next)
```

| Model | Error path | Catch-all placement | Key risk |
| ----- | ---------- | ------------------- | -------- |
| Express | `next(err)` flows to the next error-handling middleware **after** the thrower | Registered last, after all routes | Placing it early means later routes are uncovered |
| Koa | `try { await next() } catch` wraps everything downstream | Outermost (registered first) | Must `try/catch` around `await next()`; a later catch is too late |
| Fastify | `setErrorHandler` is centralized per encapsulation scope | On the root instance (or per plugin) | A plugin's own handler can shadow the parent's |

The unifying rule: **the catch-all must be able to observe every error.** How you achieve that
depends on the model.

## How it works — Express, in detail

Express middleware run in registration order. Error-handling middleware are identified by their
**four-argument** signature `(err, req, res, next)`, and they only receive errors thrown by
layers registered **before** them.

```ts
app.use(requestId());                 // 1. correlation first
app.use(sizeGuard(1_048_576));        // 2. reject before buffering
app.use(contentTypeGuard());          // 3. reject before parsing
app.use(express.json());              // 4. parse
app.use(authenticate());              // 5. principal
app.use(authorize());                 // 6. permission
app.use(rateLimitByTenant());         // 7. identity-keyed limit

app.use("/api/v1", router);           // 8. routes

app.use(notFoundHandler);             // 9. unmatched routes → 404 problem
app.use(globalErrorHandler);          // 10. catch-all LAST
```

Consequences:

- **Layer 10 catches errors from layers 1–9.** An error thrown by a layer registered after the
  error handler is *not* caught by it; it falls to the framework default.
- **`next(err)` is the propagation mechanism.** Synchronous throws in an async handler are **not**
  caught by Express 4 automatically; wrap async handlers or the boundary won't see them.
- **A response already sent** is not a special case as far as Express is concerned — it will call
  your handler, and your handler must check `res.headersSent`.

```ts
function globalErrorHandler(err: unknown, req: Request, res: Response, next: NextFunction) {
  if (res.headersSent) {
    req.log?.error({ err }, "error after headers sent");
    return res.destroy();
  }
  const problem = buildProblem(err, { instance: req.originalUrl, requestId: req.id });
  sendProblem(res, problem);
  // do NOT call next(err) — that hands off to the framework default
}

// Async handler wrapper Express 4 needs so rejections reach the boundary.
const wrap = (fn: RequestHandler): RequestHandler =>
  (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
```

> ⚠️ **Hazard.** Calling `next(err)` at the end of the catch-all invokes the framework's default
> error handler, which usually renders HTML or a stack. The catch-all is terminal; it must not
> forward.

## How it works — Koa, in detail

Koa composes middleware as an onion: each middleware does its work, `await next()`, then does
post-work. Errors thrown downstream surface as rejections of the `next()` promise, so *any*
middleware can catch them by wrapping `await next()`.

```ts
app.use(async (ctx, next) => {           // 1. catch-all OUTERMOST
  try {
    await next();
  } catch (err) {
    if (ctx.headerSent) {
      ctx.app.emit("error", err, ctx);   // log; cannot change the response
      ctx.res.destroy();
      return;
    }
    sendProblem(ctx, buildProblem(err, { instance: ctx.path, requestId: ctx.state.id }));
  }
});

app.use(async (ctx, next) => { ctx.state.id = genRequestId(); await next(); });
app.use(sizeGuard());
app.use(contentTypeGuard());
app.use(bodyParser());
app.use(authenticate());
app.use(authorize());
app.use(rateLimitByTenant());
app.use(router.routes());
```

Consequences:

- **The catch-all is registered first** so its `try` wraps everything inside it. Registering it
  *last* would wrap nothing and catch nothing.
- **Post-work order is reversed.** A middleware registered second runs its pre-work first-after-
  first and its post-work after the handler — useful for timing, response transforms, and
  transactional wrappers.
- **`ctx.headerSent`** is Koa's `res.headersSent` equivalent.

## How it works — Fastify, in detail

Fastify does not use a promise-composed chain for errors; it uses **hooks** for lifecycle and a
centralized `setErrorHandler` per encapsulation scope.

- **Hooks** (`onRequest`, `preParsing`, `preValidation`, `preHandler`, `onSend`, `onError`) run
  in a documented order.
- **Errors from hooks and handlers** go to the nearest `errorHandler` in the encapsulation tree;
  if none, to the parent's, up to the root.
- **Plugins are encapsulated by default:** a hook or handler registered inside a plugin does not
  apply to sibling plugins unless using `fastify-plugin` to break encapsulation.

```ts
const app = Fastify({ bodyLimit: 1_048_576 });   // size limit at the instance

app.decorateRequest("id", "");
app.addHook("onRequest", async (req) => { req.id = genRequestId(req.id); });
app.addHook("preParsing", async (req) => { assertSupportedContentType(req); });

// Catch-all: the root error handler sees errors from all routes/plugins
// unless a plugin installs its own.
app.setErrorHandler((err, req, reply) => {
  if (reply.sent) {
    req.log.error({ err }, "error after headers sent");
    return reply.raw.destroy();
  }
  const problem = buildProblem(err, { instance: req.url, requestId: req.id });
  reply
    .code(problem.status)
    .type("application/problem+json")
    .header("X-Request-Id", problem.requestId)
    .send(problem);
});

app.register(apiRoutes, { prefix: "/api/v1" });
```

Consequences:

- **`reply.sent`** is the headers-sent equivalent.
- **Per-plugin error handlers** are powerful and also a footgun: a plugin that installs its own
  handler silently stops inheriting the root one for its scope. Audit them.
- **Hook order matters:** `preParsing` is the place for size/type guards (the body limit is also
  an instance option); `preHandler` is where auth/authz commonly run.

## Ordering matrix (all three frameworks)

| Concern | Express | Koa | Fastify |
| ------- | ------- | --- | ------- |
| Request id | `app.use` first | `app.use` (wraps) | `onRequest` hook |
| Size limit | middleware / body parser `limit` | middleware / parser option | `bodyLimit` option + `preParsing` |
| Content type | guard middleware | guard middleware | `preParsing` hook |
| Parse | `express.json()` | body parser middleware | built-in parsing |
| Auth | `app.use` after parse | `app.use` after parse | `preHandler` hook |
| Authz | `app.use` | `app.use` | `preHandler` hook |
| Rate limit (identity) | after auth | after auth | `preHandler` after auth |
| Catch-all | last `(err,req,res,next)` | first `try{await next()}` | root `setErrorHandler` |

## Worked example — the same failure, three frameworks

A handler throws `ProviderUnavailable` (`503` + `Retry-After`) before any write.

```ts
// Express: error reaches the LAST-registered 4-arg handler.
app.use((err, req, res, _next) => {
  if (res.headersSent) return res.destroy();
  sendProblem(res, buildProblem(err, { instance: req.originalUrl, requestId: req.id }));
});

// Koa: error rejects next(), caught by the FIRST-registered wrapper.
app.use(async (ctx, next) => {
  try { await next(); }
  catch (err) { sendProblem(ctx, buildProblem(err, { instance: ctx.path, requestId: ctx.state.id })); }
});

// Fastify: error routed to the root setErrorHandler for the scope.
app.setErrorHandler((err, req, reply) =>
  reply.code(503).type("application/problem+json").send(
    buildProblem(err, { instance: req.url, requestId: req.id })));
```

All three produce the identical Ch. 20 document. The *mechanics* differ; the *contract* does not.

## Key data / numbers

- **Express 5** propagates rejected promises from async handlers to error middleware; Express 4
  does not — wrap async handlers with `.catch(next)`.
- **Koa** error middleware can be placed anywhere; only *outermost* placement sees all errors.
- **Fastify `bodyLimit`** defaults to **1 MiB**; the `onSend` hook runs before the body is
  written and is the last chance to modify the response.
- **Fastify encapsulation:** use `fastify-plugin` to share hooks/handlers across siblings
  deliberately.
- **Headers-sent check:** `res.headersSent` (Express), `ctx.headerSent` (Koa), `reply.sent`
  (Fastify).

## Real-world use case — Acme SaaS framework migration

Acme migrated the public API from Express 4 to Fastify for throughput. The error handler was
ported faithfully — but the app's async handlers had relied on Express's *implicit* rejection
handling (added in a wrapper), and Fastify's `setErrorHandler` was installed on a plugin rather
than the root, so sibling plugins stopped inheriting it. Two endpoints reverted to default error
output. The fix: install the handler at the root, verify encapsulation with a test that throws
from each plugin, and keep a single golden-set of error fixtures (Ch. 20 file 12) that runs against
every framework target. The contract stayed byte-identical across the migration; only the wiring
changed.

## Trade-offs

| Framework model | Pros | Cons | Best fit |
| --------------- | ---- | ---- | -------- |
| Express linear | Simple; ubiquitous | Async throws need wrapping; order footguns | Small/medium REST APIs |
| Koa onion | Elegant wrapping; timing/transforms natural | Must reason about post-work reversal | APIs wanting structured composition |
| Fastify encapsulated | Fast; explicit lifecycle hooks | Encapsulation surprises; per-plugin handlers | Performance-sensitive APIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Place the catch-all per the framework's model (last vs outermost vs root) | Copy Express ordering into Koa or Fastify |
| Check headers-sent in every framework's handler | Assume the framework prevents double-write |
| Verify plugin/hook scope with a throw-test | Trust default encapsulation blindly |
| Keep one contract fixture across frameworks | Let each framework's default render errors |
| Wrap async handlers where the framework requires | Rely on implicit rejection catching |

## Common mistakes

- **Express catch-all that calls `next(err)`.** It hands control to the default error renderer.
- **Koa catch-all registered last.** It wraps nothing downstream and catches nothing.
- **Fastify per-plugin error handler that forgets to delegate.** Its scope silently loses the
  root contract.
- **Assuming hooks and middleware are interchangeable.** They have different order, scope, and
  error propagation rules.
- **No headers-sent guard.** Every framework will still let you attempt an impossible write.

## Checklist

- [ ] Catch-all placement matches the framework model.
- [ ] Async handlers propagate rejections in the framework's required way.
- [ ] Header-sent (`headersSent`/`headerSent`/`sent`) is checked before responding.
- [ ] Plugin/hook scope is tested with a forced throw per scope.
- [ ] One golden error fixture runs against every framework target.

## Related

- [Ordering and Swallowing](../01-concepts/05-ordering-and-swallowing.md)
- [The Response-Already-Started Problem](./02-response-already-started.md)
- [Global Handlers and the Request Boundary](../01-concepts/01-global-handlers-and-the-request-boundary.md)
