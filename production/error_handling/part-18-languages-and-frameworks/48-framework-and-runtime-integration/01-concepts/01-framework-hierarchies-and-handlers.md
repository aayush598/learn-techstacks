# Framework Hierarchies and Handlers

> Part XVIII · Chapter 48 · Sections 48.1–48.4, 48.9–48.12 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 47 — Language-Level Error Semantics](../../47-language-level-error-semantics/README.md), [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)

## In one sentence

**Frameworks impose an error hierarchy on every request** — middleware, filters, exception
handlers, and lifecycle hooks run in a fixed order — and your job is to plug translation and
policy into the *right* layer without breaking that order.

## Why this matters in production

A mis-ordered middleware can swallow an exception before your error filter runs; a
`setErrorHandler` can serialize `Error.cause` to JSON (leaking internals); a startup failure can
be logged as a 500 because it never reached the bootstrap boundary. Knowing the hierarchy is
what separates "works in dev" from "fails safely in prod".

## 48.1–48.2 — Framework hierarchies and built-in handlers

Every HTTP framework has a chain: request enters, passes through middleware, reaches a
handler/controller, and failures bubble up to some form of error handler.

| Framework | Hierarchy | Built-in handler | Notes |
| --------- | ---------- | ----------------- | ----- |
| **Express (Node/TS)** | `app.use(middleware)` → routes → 4-arg `(err, req, res, next)` error middleware | Default: sends `err.stack` in dev, minimal in prod; no RFC 9457 by default | Order is critical; error middleware must be registered last |
| **Fastify (Node/TS)** | `onRequest` → preValidation/preHandler → handler → `setErrorHandler` | `setErrorHandler` receives `error`, `request`, `reply`; schema validation errors are thrown as `FST_ERR_*` | Strongly schema-driven; can use `setErrorHandler` per context |
| **NestJS (Node/TS)** | Guards → Interceptors → Pipes → Controller method → `ExceptionFilter` hierarchy | `BaseExceptionFilter` + `HttpExceptionFilter`; can define global/route/ method filters | Filters catch exceptions; exceptions thrown by pipes/guards/interceptors also go through filters |
| **Spring Boot (Java)** | Filters → `DispatcherServlet` → `HandlerInterceptor` → `@Controller` → `@ControllerAdvice`/`@ExceptionHandler` | `BasicErrorController` for `/error`; `DefaultErrorAttributes` | `@ControllerAdvice` can target packages; `ResponseEntityExceptionHandler` covers MVC exceptions |
| **Django (Python)** | Middleware stack → URL resolver → view → exception middleware → `handler500`/custom middleware | `django.views.defaults` handlers; `ExceptionMiddleware` | Middleware can process exceptions; `LOGGING` + custom middleware for structured errors |
| **ASP.NET Core (C#)** | Middleware pipeline → Endpoint routing → Action → Exception middleware/filters | Developer Exception Page, `UseExceptionHandler`, `ProblemDetails` middleware | `IExceptionHandler` (.NET 8+) is preferred over exception filters in many cases |

## 48.3–48.4 — HTTP middleware and request lifecycle

The request lifecycle is the most important map to draw on a whiteboard: **where errors can
originate, and where they can be caught.**

```text
┌─────────────┐   ┌───────────┐   ┌─────────┐   ┌───────────┐   ┌──────────────┐
│ Middleware 1 │ → │ AuthN/Z   │ → │ Parsing  │ → │ Validation │ → │ Controller/  │
│ (request id) │   │           │   │ / Body   │   │ Pipe/Schema│   │ Route Handler│
└─────────────┘   └───────────┘   └─────────┘   └───────────┘   └──────────────┘
        │                 │               │               │               │
        └─────────────────┴───────────────┴───────────────┴───────────────┘
                                        │ throws/rejects
                                        ▼
                                ┌─────────────────┐
                                │ Error Handler   │
                                │ (translate+map) │
                                └─────────────────┘
                                        │
                                        ▼
                                    HTTP Response
```

**Key data:**

- **Express:** Error middleware signature is `(err, req, res, next)` with exactly 4 args. If
  you forget the 4th parameter, Express treats it as regular middleware.
- **Fastify:** `setErrorHandler` is the single place for custom error shaping; schema errors
  carry `validation` arrays that you can map to field-level details.
- **NestJS:** Pipes can throw `BadRequestException`; guards throw; filters catch in order
  (method → controller → global). The last filter that can handle it wins.
- **Spring:** `HandlerExceptionResolver` chain; `@ExceptionHandler` methods are resolved by
  exception type; `@ControllerAdvice` applies globally.
- **Django:** Middleware can implement `process_exception(self, request, exception)` to handle
  exceptions before they reach the default handler.

## 48.9–48.12 — Startup/shutdown, defaults to preserve, conflicts

### Startup and shutdown failures

Errors during **bootstrap** are different from request errors. They must not be routed to the
HTTP error handler.

| Phase | Examples | Handling |
| ----- | -------- | -------- |
| **Config loading** | Missing env vars, invalid config schema | Fail-fast at process start; exit with non-zero code. Log once, clearly. |
| **DI / module init** | Database pool creation, Redis connect, secret fetch | Fail-fast unless the dependency is optional and you have a fallback. |
| **Migrations** | Schema mismatch | Fail-fast in most services; in some platforms gate on readiness. |
| **Graceful shutdown** | In-flight requests, job completion, connection draining | Time-bound; log remaining work; never let shutdown throw unhandled exceptions into the OS. |
| **Health/readiness** | A dependency goes down after startup | Return `503` from readiness probes; don't crash the process. |

**Real-world use case — Acme SaaS:** At startup, the billing service failed to connect to
Postgres. Because the connection error was caught by the global HTTP error middleware (due to
misordered initialization), the process logged a 500-shaped error and returned 503 to health
checks with a stack trace — obscuring "DB connection refused". Moving the DB init before
the HTTP server and failing fast with a startup-specific logger fixed it.

### Defaults to preserve vs customize

| Framework | Preserve | Customize |
| --------- | -------- | --------- |
| **Express** | Let 4xx pass through as-is if you have no mapping | Shape to RFC 9457 in one error middleware; set `Content-Type` |
| **Fastify** | Schema validation errors have a stable shape | Normalize to your envelope; don't log full schemas in prod |
| **NestJS** | Built-in `HttpException` mapping is correct for HTTP semantics | Replace `HttpExceptionFilter` globally; use `@Catch()` for your `AppError` |
| **Spring** | `ResponseEntityExceptionHandler` covers common MVC errors | Add `@ControllerAdvice` for domain errors; return `ProblemDetail` |
| **Django** | Framework exceptions map sensibly | Custom exception middleware + `handler500` with no tracebacks |

### Custom vs built-in handler conflicts

The most common conflict: **both the framework's default handler and your custom handler run**,
or your handler runs in the wrong order.

- **Express:** Register error middleware after all routes. If you call `next(err)` from
  regular middleware, it will skip route handlers and go to error middleware.
- **Fastify:** `setErrorHandler` overrides the default; child contexts can override parents.
- **NestJS:** More specific filters take precedence. A global filter will catch what route
  filters don't.
- **Order matters:** Never register a catch-all before authentication — auth failures will be
  misclassified as 500s.

## Key data / numbers

- Express error middleware requires **exactly 4 parameters**. TypeScript's types won't save
  you if you use `(...args)` incorrectly.
- Fastify's `setErrorHandler` receives validation errors with `error.validation` containing
  the JSON Schema validation details.
- NestJS exception filters are resolved by **closest scope first**: method → controller →
  module → global.
- Spring's `HandlerExceptionResolver` order can be customized; `ExceptionHandlerExceptionResolver`
  handles `@ExceptionHandler`.
- Django middleware runs in order for requests, **reverse order** for responses and exceptions.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put translation + policy in one error handler per entry point | Scatter `res.status(...)` across controllers |
| Fail fast on startup failures before binding the HTTP port | Let bootstrap errors hit the HTTP error middleware |
| Respect framework precedence (filters/middleware order) | Override order without a comment and a test |
| Preserve framework defaults until you have a reason | Replace everything on day one |
| Drain connections on shutdown with a timeout | `process.exit(0)` without waiting for in-flight work |

## Checklist

- [ ] Is there exactly one error handler per transport boundary?
- [ ] Are startup errors logged with a startup-specific logger and exit codes?
- [ ] Is middleware order documented and tested?
- [ ] Are framework validation errors normalized to your field-level format?
- [ ] Is graceful shutdown implemented with a time-bound drain?

## Related

- [Dependency Injection, ORM, and Validation Mapping](./02-dependency-injection-orm-and-validation-mapping.md)
- [Framework-Independent Policy and Adapters](./03-framework-independent-policy-and-adapters.md)
- [Custom vs Built-in Handler Conflicts](../02-deep-dive/01-custom-vs-built-in-handler-conflicts.md)
- [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
