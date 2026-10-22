# Framework-Independent Policy and Adapters

> Part XVIII · Chapter 48 · Sections 48.13–48.14 · _Estimated reading time: 16 min_
> **Prerequisite:** [Framework Hierarchies and Handlers](./01-framework-hierarchies-and-handlers.md), [Chapter 47 — Type-Safe Handling and the Common Architecture](../../47-language-level-error-semantics/02-deep-dive/02-type-safe-handling-and-common-architecture.md)

## In one sentence

**Keep taxonomy, registry, and policy in a framework-free core**; put only translation and
wiring in thin, replaceable **adapters** so swapping Express for Fastify never rewrites your
error semantics.

## Why this matters in production

Acme started on Express, moved billing routes to NestJS, and added a Fastify edge gateway.
Without adapters, each rewrite copied the status map and subtly diverged (one service returned
`422` for `DUPLICATE_RESOURCE`, another `409`). The divergence made client SDK generation
impossible and support couldn't rely on codes. Adapters enforce the dependency rule and make
the contract portable.

## 48.13 — Framework-independent policy

The policy answers: *"Given a stable error code, what should the outside world see?"* It has
no knowledge of HTTP frameworks, ORMs, or DI containers.

### What belongs in the core (framework-free)

| Component | Purpose | Example |
| --------- | ------- | ------- |
| **Error model** | The in-process representation | `AppError { code, category, retryable, cause, safeContext }` |
| **Error registry** | Code → policy mapping | `ERROR_REGISTRY[code] = { status, retryable, alert, title }` |
| **Policy functions** | Pure lookups | `policyFor(code)`, `isRetryable(err)`, `shouldAlert(err)` |
| **Translation helpers** | Pure mappers | `normalize(err)` that walks causes and returns `AppError` |
| **Error codes** | Stable vocabulary | `PAYMENT_CARD_DECLINED`, `DEPENDENCY_TIMEOUT` |

### What does NOT belong in the core

- `Request`, `Response`, `NextFunction` (Express)
- `FastifyReply`, `FastifyRequest`
- `HttpException`, `ArgumentsHost` (NestJS)
- `HttpServletRequest` (Spring)
- ORM exception classes
- DI decorators/containers

### The dependency direction rule

```text
[Framework / Transport]
          │ imports
          ▼
        [Adapters]  ← translation + wiring only
          │ imports
          ▼
         [Core]     ← policy + model + registry (zero framework deps)
```

**Rule:** `core` must have **zero imports** from framework packages. Adapters import core
and framework types. The domain/services import core types, never framework types.

## 48.14 — Reusable adapters

An adapter's job is threefold: **translate** (vendor/framework error → `AppError`), **map**
(apply policy), **serialize** (to the transport format, e.g. RFC 9457).

### Adapter responsibilities

| Step | What | Example |
| ---- | ---- | ------- |
| **1. Normalize** | Walk the cause chain, find the `AppError` or translate a framework error | `normalize(err)` checks `instanceof AppError`, else maps `ZodError`, else maps unknown to `INTERNAL_ERROR` |
| **2. Enrich** | Attach request/correlation id, tenant id (safe only) | Never attach PII or stack traces |
| **3. Policy** | Look up status, retryability, alert level | `policyFor(appErr.code)` |
| **4. Serialize** | Write the response body | RFC 9457: `type`, `title`, `status`, `detail`, `instance`, `code` |
| **5. Observe** | Log with structured fields, emit metrics/alerts | Log `error.code`, `status`, `requestId`; alert if `policy.alert` is true |

### Adapter template (language-agnostic)

```text
function handleError(err, ctx) {
  const appErr = normalize(err);        // core
  const policy = policyFor(appErr.code); // core
  const body = toProblem(appErr, policy, ctx); // adapter
  logStructured(appErr, policy, ctx);   // adapter
  if (policy.alert) alert(appErr, ctx); // adapter
  return serialize(ctx.res, policy.status, body);
}
```

### Concrete adapter sketches

**Express (TS):**

```ts
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  const appErr = normalize(err);
  const p = policyFor(appErr.code);
  res.status(p.status).type('application/problem+json').json(toProblem(appErr, p, req));
});
```

**Fastify (TS):**

```ts
fastify.setErrorHandler((err, req, reply) => {
  const appErr = normalize(err);
  const p = policyFor(appErr.code);
  reply.code(p.status).type('application/problem+json').send(toProblem(appErr, p, req));
});
```

**NestJS (TS):**

```ts
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const appErr = normalize(exception);
    const p = policyFor(appErr.code);
    ctx.getResponse().status(p.status).json(toProblem(appErr, p, ctx.getRequest()));
  }
}
```

**Spring (Java):**

```java
@ControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
  @ExceptionHandler(AppException.class)
  public ResponseEntity<ProblemDetail> handle(AppException ex, HttpServletRequest req) {
    var p = policyFor(ex.code());
    var body = toProblem(ex, p, req);
    return ResponseEntity.status(p.status()).body(body);
  }
}
```

### Testing adapters in isolation

Adapters are trivial to unit test: pass in a `ZodError`, assert `422` with field details;
pass in `PrismaClientKnownRequestError` P2002, assert `409` with `DUPLICATE_RESOURCE`; pass
in an unknown `Error`, assert `500` with `INTERNAL_ERROR` and no stack trace in the body.

## Key data / numbers

- **RFC 9457** is the standard for `application/problem+json`. Fields: `type`, `title`,
  `status`, `detail`, `instance`. Extensions like `code` and `errors` are common and safe.
- The core should have **0** framework dependencies — enforce with `eslint-plugin-import` /
  dependency-cruiser in CI.
- One adapter per transport is usually enough; avoid per-route error handlers.

## Real-world use case — Acme SaaS

Acme had three HTTP services with different error shapes. After extracting policy to a core
module and writing adapters for Express and NestJS, a client SDK could be generated from the
problem schema once. When they added a Fastify gateway, the adapter was written in half a day
with no changes to services or the domain. Incident post-mortems now reference codes, not
framework-specific error class names.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep core framework-free | Import `express` into `src/core/` |
| Translate in adapters; normalize in pure functions | Put translation logic in controllers |
| Use RFC 9457 as the wire format | Invent a new envelope per service |
| Return `code` in the problem details for machine clients | Expose internal class names or stack traces |
| Make adapters thin (wiring only) | Put business decisions in the filter/middleware |

## Checklist

- [ ] Does `core/` compile with zero framework imports?
- [ ] Is there a single `policyFor()` used by all adapters?
- [ ] Does each adapter normalize unknown errors to `INTERNAL_ERROR`?
- [ ] Is the wire format consistent across transports?
- [ ] Are adapters unit-testable without starting a server?

## Related

- [Framework Hierarchies and Handlers](./01-framework-hierarchies-and-handlers.md)
- [Dependency Injection, ORM, and Validation Mapping](./02-dependency-injection-orm-and-validation-mapping.md)
- [Custom vs Built-in Handler Conflicts](../02-deep-dive/01-custom-vs-built-in-handler-conflicts.md)
- [Express, Fastify, and NestJS Adapters](../03-practical-examples/01-express-fastify-and-nestjs-adapters.md)
- [Chapter 47 — Type-Safe Handling and the Common Architecture](../../47-language-level-error-semantics/02-deep-dive/02-type-safe-handling-and-common-architecture.md)
