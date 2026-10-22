# The Machinery of Centralized Handling

> Part IV · Chapter 10 · Sections 10.3–10.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Centralized and Local Handling](./01-centralized-vs-local-handling.md)

## In one sentence

Global exception handling, framework handlers, middleware, interceptors, decorators, and shared
utilities are **six packaging options for the same two central jobs** — *catch at the edge* and
*serialize consistently* — and picking the wrong package is what makes error handling feel like
magic.

## Why this matters in production

Every framework ships its own collection of these mechanisms, and teams stack them without a
map: middleware that catches, an interceptor that rewrites, a filter that serializes, a
decorator that logs — four transformations of one error, occasionally two response bodies. When
a status code is wrong, you cannot say which of the four decided it.

Naming each mechanism's **single job** turns the stack into a pipeline you can reason about —
and lets you reuse the same policy across Express, NestJS, FastAPI, or Gin without rewriting it.

## Core concept — the six mechanisms

| # | Mechanism | What it is | Central job (only this) |
| - | --------- | ---------- | ----------------------- |
| 10.3 | **Global exception handling** | one process-wide handler for uncaught errors | the safety net: unclassified → envelope + `500` |
| 10.4 | **Framework handlers** | the framework's built-in hook (Express error middleware, NestJS `ExceptionFilter`, FastAPI `exception_handler`, ASP.NET middleware) | adapt *our* policy to *their* lifecycle |
| 10.5 | **Middleware** | functions layered around routing | catch parsing/auth/size failures **before** handlers; hand decided errors to the serializer |
| 10.6 | **Interceptors** | wrap a handler's execution (NestJS interceptors, axios response interceptors) | normalize *outcomes* (thrown or returned) into `AppError` |
| 10.7 | **Decorators** | annotations that wrap a method/function | **local** policy attachment (`@Retryable`, `@Idempotent`) or one central concern (`@SerializeProblem`) |
| 10.8 | **Utilities / shared abstractions** | pure functions and small classes | `normalize()`, `toProblem()`, redaction — the actual reusable core |

The dependency direction matters: **10.3–10.7 all call 10.8.** If your serializer lives inside
the filter, no other entry point (CLI, worker, webhook) can reuse it.

```text
 middleware ──┐
 interceptor ─┼──▶  framework adapter  ──▶  toProblem() / normalize()  ──▶  error registry
 filter ──────┘        (10.3–10.6)              (10.8)                        (Part III/IV)
 decorator ──── local policy (retry/idempotency) — does NOT serialize
```

## How it works — one job per mechanism

### 10.3 — Global exception handling

The last in-process net. In Node, that includes `process.on("uncaughtException")` (Ch. 9, 9.12);
in a web framework, the terminal filter. Contract: render `500` + correlation ID, log with
`cause`, never leak, never decide business policy.

### 10.4 — Framework handlers

Adapt our policy to the framework's shape:

```ts
// Express — error middleware MUST take four arguments to be recognized as such
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) return next(err);            // never double-serialize
  const e = normalize(err);
  res.status(STATUS[e.code] ?? 500).json(toProblem(e, req.id));
});
```

```python
# FastAPI — one handler per exception class, registered once at startup
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status = STATUS.get(exc.code, 500)
    return JSONResponse(status_code=status,
                        content=to_problem(exc, request.state.correlation_id))
```

```ts
// NestJS — an exception filter is the framework's global handler slot
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    if (res.headersSent) return;
    const e = normalize(exception);
    res.status(STATUS[e.code] ?? 500).json(toProblem(e, requestId(ctx)));
  }
}
```

### 10.5 — Middleware

Middleware is the right place for **edge preconditions** (parse, authenticate, rate-limit) and
for handing already-decided errors downward to the serializer — never for business branching.
Ordering is the whole game; the deep dive covers it.

### 10.6 — Interceptors

Interceptors normalize *shapes*, not decisions. An axios interceptor on the way out can attach
the correlation ID and deadline; on the way in it converts a transport failure into
`UPSTREAM_UNAVAILABLE` before application code sees it. A NestJS interceptor can wrap a handler's
thrown-or-returned outcome into a uniform result. They must not retry or compensate.

### 10.7 — Decorators

Decorators attach **policy at a declaration site**, which makes them local by default:

```ts
@Retryable({ attempts: 2, retryOn: ["UPSTREAM_RATE_LIMITED"] })   // local, explicit, auditable
async charge(checkout: Checkout) { ... }
```

The one legitimate central decorator is a serialization concern applied uniformly
(`@SerializeProblem()` on controllers) — still delegating to 10.8.

### 10.8 — Utilities and shared abstractions

The heart of centralization — small, dependency-free, importable from anywhere:

```ts
// core/errors/http.ts — pure functions, zero framework imports
export const STATUS: Record<string, number> = {
  RECORD_NOT_FOUND: 404, DUPLICATE_KEY: 409, VALIDATION_FAILED: 422,
  UPSTREAM_RATE_LIMITED: 429, DB_UNAVAILABLE: 503,
};
export function toProblem(e: AppError, reqId: string) { /* RFC 9457 shape */ }
export function redact<T>(obj: T): T { /* strip secrets/PII per allowlist */ }
```

Workers, CLIs, and webhook consumers import these directly — which is what "centralized" should
mean: **one implementation, many callers**, not one giant handler.

## Key data / numbers

- Express: error middleware is recognized **only** with 4 parameters; `res.headersSent` must be
  checked or Node raises `ERR_HTTP_HEADERS_SENT` on a second write.
- FastAPI: `HTTPException(status_code=...)` for framework-level errors; custom handlers are
  registered per exception class at startup; Starlette's default handler returns
  `{"detail": "..."}` — replace it, don't fight it.
- NestJS: filters bind at controller/global scope (`@Catch()` catch-all), interceptors run
  **before** filters in the response path; pipes run before interceptors.
- RFC 9457 fields: `type`, `title`, `status`, `detail`, `instance` (+ vendor extensions).
- Recommendation: **one** global catch-all per process; additional nets are incident generators.

## Real-world use case — Acme SaaS `WebhookIngest`

`WebhookIngest` had four mechanisms stacked: body middleware, an axios interceptor, a NestJS
filter, and a decorator — each appending `" [handled]"` to messages, and two of them writing
response bodies. Stripe retries fired up to **3×** per event because duplicate `200`s and `500`s
were mixed by the second writer.

The cleanup: middleware only verified the signature and rejected `400` on failure; the
interceptor normalized SDK errors; the filter serialized via `toProblem()` after a
`headersSent` check; the decorator was deleted. One writer, one envelope, Stripe retry rate
normalized to the documented behavior.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Thin adapters + fat pure utilities (recommended) | Reusable across HTTP/worker/CLI | Requires framework glue per entry point | Default |
| Fat global filter, no utilities | One visible place | Unusable outside HTTP; untestable without a request | Small scripts |
| Decorator-heavy policy | Declarative, local | Ordering magic; hard to trace | Where the framework is decorator-native (NestJS) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep serializers/redaction as pure utilities | Bury them inside one filter class |
| Let exactly one mechanism write the body | Let middleware *and* filter serialize |
| Check `headersSent` before writing | Write a second response after headers left |
| Attach local policy with explicit decorators | Hide global side effects in decorators |

## Common mistakes

- **Middleware swallowing** — catching an error, logging, and returning `200` "to be safe."
- **Interceptor retrying** — resiliency belongs in the application or an explicit client policy
  (Chapter 27), not in a shape-normalizing wrapper.
- **Filter importing every domain error class** — the coupling deep dive (10.12–10.13) shows the
  fix: depend on the registry, not on types.

## Checklist

- [ ] Each mechanism in your stack has exactly one documented job.
- [ ] Serializers and redaction live in framework-free utilities.
- [ ] Only one layer writes the error response body.
- [ ] `headersSent` (or equivalent) is checked before serialization.

## Related

- [Centralized and Local Handling](./01-centralized-vs-local-handling.md)
- [Composition, Ordering, and Fallthrough](../02-deep-dive/02-composition-ordering-and-fallthrough.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 48 — Framework and Runtime Integration](../../../part-18-languages-and-frameworks/48-framework-and-runtime-integration/README.md)
