# A Complete Middleware Chain

> Part VIII · Chapter 21 · Sections 21.1–21.18 applied · _Estimated reading time: 22 min_
> **Prerequisite:** [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)

## In one sentence

This walkthrough assembles a full TypeScript middleware chain — request id, size and type
guards, parsing, auth, authz, rate limiting, routes, and a terminal catch-all — such that
**every path, including parser and framework errors, ends in one Ch. 20 Problem Details document
or a deliberate abort.**

## Why this matters in production

Reading the rules is not the same as wiring them. A real chain has to decide where each guard
lives, how errors propagate, and how the catch-all detects a committed head — and it must do so
in one consistent order. The code below is Express-flavored, runnable-in-spirit TypeScript; the
shape (typed errors + one boundary) ports to Koa and Fastify with only the registration
mechanics changing. Adapt it rather than import it.

## Core concept — the chain as a pipeline

```text
requestId()  →  sizeGuard()  →  contentTypeGuard()  →  parseJson()
    →  authenticate()  →  authorize()  →  rateLimit()  →  router
                        →  notFound()  →  globalErrorHandler()   (terminal)
```

Every guard either calls `next()` or `next(typedError)`. **No guard writes a response.** Only
`sendProblem` (the boundary) and the deliberate Zone C abort write anything.

## Step 1 — typed errors and the boundary

```ts
// errors.ts — internal shapes. Never serialized directly.
export class HttpError extends Error {
  constructor(readonly code: string, readonly meta?: Record<string, unknown>) {
    super(code);
    this.name = "HttpError";
  }
}
export const authError = (code: string) => new HttpError(code);
export const payloadTooLarge = () => new HttpError("PAYLOAD_TOO_LARGE");
export const unsupportedMedia = () => new HttpError("UNSUPPORTED_MEDIA_TYPE");
export const malformedJson = () => new HttpError("MALFORMED_JSON");
```

```ts
// problem .ts — the only thing allowed on the wire (see Ch. 20 file 01).
export type PublicProblem = {
  type: string; title: string; status: number;
  detail: string; instance: string; code: string; requestId: string;
  errors?: { field: string; code: string; message: string }[];
  retryAfterSeconds?: number;
};

const META: Record<string, { type: string; title: string; status: number }> = {
  MALFORMED_JSON:           { type: "/problems/malformed-request",     title: "Malformed Request",     status: 400 },
  PAYLOAD_TOO_LARGE:        { type: "/problems/payload-too-large",     title: "Payload Too Large",     status: 413 },
  UNSUPPORTED_MEDIA_TYPE:   { type: "/problems/unsupported-media-type",title: "Unsupported Media Type",status: 415 },
  TOKEN_MISSING:            { type: "/problems/unauthenticated",       title: "Unauthenticated",       status: 401 },
  TOKEN_EXPIRED:            { type: "/problems/unauthenticated",       title: "Unauthenticated",       status: 401 },
  INSUFFICIENT_ROLE:        { type: "/problems/forbidden",             title: "Forbidden",             status: 403 },
  RESOURCE_NOT_FOUND:       { type: "/problems/not-found",             title: "Not Found",             status: 404 },
  RATE_LIMITED:             { type: "/problems/rate-limited",          title: "Too Many Requests",     status: 429 },
  INTERNAL_ERROR:           { type: "/problems/internal-error",        title: "Internal Server Error", status: 500 },
};

export function buildProblem(err: unknown, ctx: { instance: string; requestId: string }): PublicProblem {
  const code = err instanceof HttpError ? err.code : "INTERNAL_ERROR";
  const meta = META[code] ?? META.INTERNAL_ERROR;
  const problem: PublicProblem = {
    type: meta.type, title: meta.title, status: meta.status,
    detail: detailFor(code), instance: ctx.instance, code, requestId: ctx.requestId,
  };
  const retry = (err as HttpError)?.meta?.retryAfterSeconds;
  if (typeof retry === "number") problem.retryAfterSeconds = retry;
  return problem;
}

function detailFor(code: string): string {
  switch (code) {
    case "MALFORMED_JSON":        return "The request body is not valid JSON.";
    case "PAYLOAD_TOO_LARGE":     return "The request body exceeds the 1 MiB limit.";
    case "UNSUPPORTED_MEDIA_TYPE":return "This endpoint accepts application/json only.";
    case "TOKEN_EXPIRED":         return "The access token expired. Refresh and retry.";
    case "INSUFFICIENT_ROLE":     return "You do not have permission for this action.";
    case "RATE_LIMITED":          return "Rate limit exceeded. Retry after the given delay.";
    case "INTERNAL_ERROR":        return "An unexpected error occurred. Provide the requestId to support.";
    default:                      return "The request could not be completed.";
  }
}
```

`buildProblem` never reads `err.stack`, `err.message`, or `err.cause`; unknown errors collapse to
`INTERNAL_ERROR`. The serializer output is a plain object.

## Step 2 — the guards

```ts
const MAX_JSON_BYTES = 1_048_576;

export function requestId() {
  return (req: Request, res: Response, next: NextFunction) => {
    const id = `req_${randomBytes(12).toString("hex")}`;   // opaque, non-sequential
    (req as any).id = id;
    res.setHeader("X-Request-Id", id);
    next();
  };
}

export function sizeGuard(limit = MAX_JSON_BYTES) {
  return (req: Request, res: Response, next: NextFunction) => {
    const declared = Number(req.headers["content-length"] ?? "0");
    if (Number.isFinite(declared) && declared > limit) return next(payloadTooLarge());
    let seen = 0;
    req.on("data", (c: Buffer) => {
      seen += c.length;
      if (seen > limit) { req.destroy(); next(payloadTooLarge()); }
    });
    next();
  };
}

export function contentTypeGuard() {
  const methodHasBody = (m?: string) => ["POST", "PUT", "PATCH"].includes(m ?? "");
  return (req: Request, _res: Response, next: NextFunction) => {
    if (!methodHasBody(req.method)) return next();
    const ct = (req.headers["content-type"] ?? "").split(";")[0].trim().toLowerCase();
    if (ct !== "application/json") return next(unsupportedMedia());
    next();
  };
}

export function parseJson() {
  const parser = express.json({ limit: MAX_JSON_BYTES });
  return (req: Request, res: Response, next: NextFunction) =>
    parser(req, res, (err: unknown) => (err ? next(malformedJson()) : next()));
}
```

`parseJson` normalizes any parser error to `MALFORMED_JSON` — the parser's own `SyntaxError`
never reaches the client.

## Step 3 — auth, authz, rate limit

```ts
export function authenticate() {
  return (req: Request, _res: Response, next: NextFunction) => {
    const h = req.headers.authorization;
    if (!h?.startsWith("Bearer ")) return next(authError("TOKEN_MISSING"));
    try {
      (req as any).principal = verifyToken(h.slice(7));   // throws TokenExpired etc.
      next();
    } catch (err) {
      next(toAuthError(err));                               // IdP outage → 503, not 401
    }
  };
}

export function authorize(action: string) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const p = (req as any).principal;
    if (!p?.can(action)) {
      const hide = action.startsWith("tenant:");
      return next(authError(hide ? "RESOURCE_NOT_FOUND" : "INSUFFICIENT_ROLE"));
    }
    next();
  };
}

export function rateLimit(limit: number, windowSec: number) {
  return async (req: Request, _res: Response, next: NextFunction) => {
    try {
      const key = (req as any).principal?.tenantId ?? "anon";
      const { allowed, retryAfter } = await bucket(key, limit, windowSec);
      if (!allowed) return next(new HttpError("RATE_LIMITED", { retryAfterSeconds: retryAfter }));
      next();
    } catch {
      next(new HttpError("SERVICE_UNAVAILABLE"));          // limiter store down: fail closed
    }
  };
}
```

## Step 4 — the terminal boundary

```ts
export function notFound() {
  return (_req: Request, _res: Response, next: NextFunction) =>
    next(new HttpError("ROUTE_NOT_FOUND"));                 // registry: 404
}

export function globalErrorHandler() {
  return (err: unknown, req: Request, res: Response, _next: NextFunction) => {
    const requestId = (req as any).id ?? "req_unknown";

    if (res.headersSent) {
      // Zone C: head committed. Log and abort; never write a second response.
      (req as any).log?.error({ err, requestId }, "error after headers sent");
      if (!res.writableEnded) res.destroy();
      return;
    }

    const problem = buildProblem(err, { instance: req.originalUrl, requestId });
    if ((req as any).log) (req as any).log.error({ err, requestId }, "request failed");
    res.status(problem.status)
       .set("Content-Type", "application/problem+json")
       .set("X-Request-Id", problem.requestId);
    if (typeof problem.retryAfterSeconds === "number") {
      res.set("Retry-After", String(problem.retryAfterSeconds));
    }
    res.send(JSON.stringify(problem));
  };
}
```

Notes: no `next(err)` at the end (that would call the framework default); the 500 detail is
generic; `Retry-After` mirrors `retryAfterSeconds`.

## Step 5 — wiring it

```ts
const app = express();

app.use(requestId());                 // correlation first
app.use(sizeGuard());                 // reject before buffering
app.use(contentTypeGuard());          // reject before parsing
app.use(parseJson());                 // parse (normalizes parser errors)

app.use(authenticate());              // principal
app.use(authorize("projects:write")); // permission
app.use(rateLimit(120, 60));          // identity-keyed limit

app.use("/api/v1", router);           // routes
app.use(notFound());                  // unmatched → 404 problem
app.use(globalErrorHandler());        // catch-all LAST (Express model)
```

Async handlers must propagate rejections:

```ts
const wrap = (fn: RequestHandler): RequestHandler =>
  (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.post("/api/v1/projects", wrap(async (req, res) => {
  const project = await projects.create((req as any).principal, req.body); // may throw
  res.status(201).json(project);
}));
```

## End-to-end traces

**Malformed JSON → `400`:**

```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
X-Request-Id: req_5c1e

{ "type": "/problems/malformed-request", "title": "Malformed Request",
  "status": 400, "detail": "The request body is not valid JSON.",
  "instance": "/api/v1/projects", "code": "MALFORMED_JSON", "requestId": "req_5c1e" }
```

**Oversized body → `413`** (rejected at `sizeGuard`, before parsing).

**Expired token → `401`** with `WWW-Authenticate: Bearer error="invalid_token"`.

**Missing tenant scope → `404`** (hiding policy), **role missing → `403`**.

**Throttled → `429`** with `Retry-After`; **handler bug → `500`** with the generic
`INTERNAL_ERROR` document and `requestId`; **stream failure after commit → abort** (logged).

## Key data / numbers

- **`MAX_JSON_BYTES` = 1 MiB** default; uploads use a separate streamed path.
- **`requestId`** = opaque random hex; equal in header and body by construction.
- **`Retry-After`** set for `429`/`503` from `retryAfterSeconds`.
- **Unknown errors** → `INTERNAL_ERROR` `500`; never a stack or raw message.
- **Express 4** needs the `wrap` helper for async handlers; Express 5 does not.

## Real-world use case — Acme SaaS one-chain rollout

Acme had four endpoints that answered errors themselves (`res.status(400).json({error})`) and one
route that caught everything and returned `200 {ok:false}`. This chain removed those five
hand-rolled shapes in an afternoon: guards and handlers now only `next(typedError)`, and the
boundary owns every response. Ch. 20's golden-set contract tests pass byte-for-byte except
`requestId`. The two bugs the rollout surfaced were exactly the ones the chapter predicts: a route
registered *after* an early-placed error handler (uncovered), and an async handler whose
rejection Express 4 did not catch (fixed with `wrap`).

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Normalize parser/framework errors in the guards | Let `SyntaxError` text reach the client |
| Generate `requestId` first, reuse it everywhere | Create a new id in the boundary |
| Keep all responses in `sendProblem`/the boundary | Answer errors inside middleware/handlers |
| Check `headersSent` and abort on Zone C | Attempt a second body after commit |
| Wrap async handlers where required | Rely on implicit rejection catching |
| Mirror `Retry-After` with `retryAfterSeconds` | Return `429`/`503` without a delay |

## Checklist

- [ ] Guards only `next(typedError)`; the boundary is the sole writer.
- [ ] Order is id → size → type → parse → auth → authz → limit → routes → 404 → catch-all.
- [ ] Parser errors normalize to `MALFORMED_JSON` (no parser text echoed).
- [ ] Catch-all checks `headersSent`, aborts on Zone C, never calls `next(err)`.
- [ ] Async handlers propagate rejections for the framework version in use.
- [ ] Golden-set contract tests pass against the chain.

## Related

- [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)
- [Handling 413, 415, 400, and Client Aborts](./02-handling-413-415-400-and-aborts.md)
- [The Problem Details Envelope in Code (Ch. 20)](../../20-standardized-api-error-responses/03-practical-examples/01-problem-details-envelope-in-code.md)
