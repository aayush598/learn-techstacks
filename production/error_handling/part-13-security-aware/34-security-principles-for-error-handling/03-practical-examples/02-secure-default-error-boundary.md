# Practical — Secure-Default Error Boundary

> Part XIII · Chapter 34 · Sections 34.16–34.18 · _Estimated reading time: 19 min_
> **Prerequisite:** [Error Sanitizer and Allowlist Serializer](./01-error-sanitizer-allowlist-serializer.md)

## In one sentence

A **secure-default error boundary** is the outermost handler that guarantees every unknown failure
becomes a generic external response with a correlation ID, routes full detail to internal sinks,
**fails closed** on security paths, and applies **tiered detail** for authenticated users, tenant
admins, and operators.

## Why this matters in production

Individual catch blocks cannot be trusted to be safe — there are too many, and they are written under
time pressure. The boundary is the one place that *must* be safe, so the whole system's disclosure
guarantee reduces to "does the boundary hold?". If it does, a careless `throw` deep in the domain
cannot leak; if it does not, every other control is defeated.

## Design principles

| Principle | Meaning at the boundary |
| --------- | ----------------------- |
| **Secure default** | Unknown error → generic `500` + `requestId` |
| **Fail closed** | Auth/authz path errors → deny, never allow |
| **Tiered detail** | Response detail depends on the audience, resolved here |
| **Single sink router** | All channels fed from one place |
| **Never throws** | The boundary itself must not fail |

## The boundary

```ts
import { randomUUID } from "node:crypto";

type Audience = "public" | "user" | "tenantAdmin" | "operator";

function resolveAudience(req: Request): Audience {
  if (req.auth?.role === "operator") return "operator";
  if (req.auth?.role === "tenantAdmin") return "tenantAdmin";
  if (req.auth) return "user";
  return "public";
}

// Tiered response projection: what detail each audience may see.
function respond(err: unknown, audience: Audience): { status: number; body: unknown } {
  const isSecPath = isSecurityPath(err);       // auth/authz classes
  const known = isAppError(err) && err.disclosure !== "internal";

  // Secure default for anything unknown or marked internal-only.
  if (!known || isSecPath) {
    const base = {
      code: isSecPath ? "FORBIDDEN_OR_NOT_FOUND" : "INTERNAL_ERROR",
      message: isSecPath
        ? "You do not have access to this resource."
        : "Something went wrong. Please try again.",
    };
    // Operators get the real code; everyone else gets the safe default.
    if (audience === "operator" && isAppError(err)) {
      return { status: err.httpStatus, body: { code: err.code, class: err.class } };
    }
    return { status: isSecPath ? 404 : 500, body: base };
  }

  const body: Record<string, unknown> = { code: err.code, message: err.safeMessage };
  if (audience !== "public") body.detail = err.publicDetail; // authenticated may see more
  return { status: err.httpStatus, body };
}

export function errorBoundary(err: unknown, req: Request, res: Response) {
  const cid = req.id ?? randomUUID();
  const audience = resolveAudience(req);

  // Internal sinks get full detail; external response is tiered and safe.
  try {
    log.error(sanitize(err, "log"), "boundary caught error");
    trackError({ ...sanitize(err, "tracker"), requestId: cid, audience });
    metrics.increment("errors_total", sanitize(err, "metric"));
  } catch (sinkError) {
    // A sink failure must never change the external outcome.
    log.error({ code: "SINK_FAILURE" }, "failed to record error");
  }

  const { status, body } = respond(err, audience);
  if (!res.headersSent) {
    res.status(status).json({ ...body, requestId: cid });
  }
}
```

Key properties visible in the code:

- **`respond` fails safe**: unknown or internal-only errors never echo `err.message`.
- **Security paths collapse to a uniform `404`** (see
  [Chapter 35](../../35-auth-authorization-and-tenant-isolation-errors/README.md)) regardless of the
  true cause, so the boundary cannot confirm existence.
- **Sink failures are isolated**: a broken log/metric call does not change what the user sees.
- **`requestId` is always emitted**, so support correlates without disclosure.

## Fail-closed on security paths

```ts
function isSecurityPath(err: unknown): boolean {
  return isAppError(err) && (err.class === "auth" || err.class === "authz");
}

// In middleware, an unexpected error in the permission check must DENY.
app.use("/api/*", (req, res, next) => {
  try {
    const decision = policyEngine.can(req.auth, req.path);
    if (!decision.allow) return next(new AuthzError());
    next();
  } catch (e) {
    // Do NOT continue. An error in the check is a denial, not a pass.
    next(new AuthzError({ cause: e }));
  }
});
```

The dangerous alternative — `catch (e) { next(); }` — turns a policy-engine outage into a
**fail-open** authorization bypass. The boundary and the middleware must agree on fail-closed.

## Tiered detail in practice

| Audience | Unknown error | Known public error | Own 404 | Other-tenant 404 |
| -------- | ------------- | ------------------ | ------- | ---------------- |
| public | generic 500 | code + message | 404 | 404 (identical) |
| user | generic 500 | code + message + detail | 404 | 404 (identical) |
| tenantAdmin | generic 500 | code + message + detail | 404 | 404 (identical) |
| operator | real code + class | full known shape | 404 | 404 (identical) |

The **other-tenant 404 must be byte-identical** to the own-resource 404 for public/user/admin — any
difference recreates the existence oracle.

## Async and worker boundaries

Request handlers are not the only boundary. Apply the same secure default in workers and consumers:

```python
def job_boundary(job, run):
    try:
        run(job)
    except Exception as exc:                      # unknown failure
        # External shape is generic; job record keeps internal detail for operators.
        job.fail(code="INTERNAL_ERROR", terminal_reason="permanent")
        log.error({"job_type": job.type, "tenant": job.tenant_id, "code": "JOB_FAILED"})
        track_error(sanitize(exc, "tracker"), job_id=job.id)
        raise                                     # let the queue apply its retry/DLQ policy
```

## Key data / numbers

- **HTTP secure defaults**: unhandled → `500`; security path → uniform `404`; known invalid input →
  `4xx` with a public code. Never `200` for a failure.
- **`requestId`** must be attached to every external error and the matching internal records; a >99%
  join rate is a reasonable target.
- **OWASP A05 / A09**: generic external errors and structured internal logging are the recognized
  mitigations; the boundary is where both are enforced.
- **Fail-open** is a recognized critical anti-pattern in authorization middleware; log and alarm on
  it (`policy_engine_error_total`).

## Real-world use case — Acme SaaS

Acme's authorization middleware wrapped its policy-engine call in a `try/catch` that called `next()`
on error. During a policy-engine outage, all authorization checks passed and every tenant could read
every workspace for eleven minutes. Fix: the catch now constructs an `AuthzError` (fail-closed), the
boundary collapses all authz errors to a uniform `404`, and a metric `authz_check_error_total` pages
on any policy-engine error. A test injects a policy-engine exception and asserts the response is
`404` and the request is **not** allowed through. The boundary + middleware change closed a live
authorization bypass.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single boundary with tiers | One place to audit | More logic in one function | Default |
| Per-handler error shaping | Local control | Inconsistent, easy to leak | Small apps only |
| Fail-open authz | Availability | Authorization bypass | Never |

## Common mistakes

- **`res.status(...)` after headers sent.** Guard with `headersSent`.
- **Boundary that throws.** Wrap sink calls in `try/catch`.
- **Different 404 bodies for owned vs other-tenant.** Recreates the oracle.
- **Fail-open middleware.** The most dangerous single line in this chapter.
- **No `requestId`.** Support cannot debug without you disclosing.

## Checklist

- [ ] Is there one outermost boundary per request/worker?
- [ ] Does an unknown error always produce a generic response + `requestId`?
- [ ] Do auth/authz errors collapse to a uniform `404` for non-operators?
- [ ] Is the boundary's own sink logic failure-isolated?
- [ ] Does authorization middleware fail **closed**?
- [ ] Is the other-tenant 404 byte-identical to the owned 404?

## Related

- [Error Sanitizer and Allowlist Serializer](./01-error-sanitizer-allowlist-serializer.md)
- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Glossary](../../../GLOSSARY.md)
