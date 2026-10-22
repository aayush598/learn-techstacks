# Auth, Authz, and Rate-Limit Middleware

> Part VIII · Chapter 21 · Sections 21.3, 21.4, 21.5 · _Estimated reading time: 17 min_
> **Prerequisite:** [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)

## In one sentence

Authentication establishes **who** (21.3), authorization decides **what they may do** (21.4),
and rate limiting protects the system from **too much** (21.5) — and their **order matters**:
authenticate before identity-keyed rate limits, and authorize after parsing when the decision
depends on the body.

## Why this matters in production

These three middleware are where error handling and security meet, so mistakes are expensive.
Returning `401` for a permission problem tells a client to refresh a token that was never the
issue. Rate-limiting on IP before authentication lets a shared NAT punish thousands of innocent
users while a distributed attacker rotates addresses. Running authorization on a body the parser
has not validated yet means you authorize against garbage — or crash. Getting the order and the
classification right is what makes the responses correct *and* safe.

## Core concept — identity, permission, quota

| Middleware | Question | Fails with | Required headers |
| ---------- | -------- | ---------- | ---------------- |
| Auth (21.3) | "Who are you, and is the credential valid?" | `401` | `WWW-Authenticate` |
| Authz (21.4) | "May this identity perform this action on this resource?" | `403` (or `404` to hide) | — |
| Rate limit (21.5) | "Has this key exceeded its quota?" | `429` | `Retry-After` |

The canonical order for a body-bearing, identity-aware API:

```text
routing → size guard → content-type guard → parse → AUTH → AUTHZ → RATE LIMIT → handler
```

Two caveats:

- **If rate limiting is per-IP and cheap, it may run before auth** to shed load early. If it is
  per-identity/per-tenant, it must run **after** auth. Choose deliberately; you cannot key a limit
  on a principal you have not identified.
- **Authz that depends on the body** must run after parsing. Authz that depends only on
  path/method/headers can run before, but keeping one order is simpler and safer.

## 21.3 — Authentication middleware

Authentication resolves a credential to a principal (a user, service account, or API key),
usually attaching it to the request context.

Failure modes and their codes:

| Condition | Status | Code (example) | Header |
| --------- | ------ | -------------- | ------ |
| No credential presented | `401` | `TOKEN_MISSING` | `WWW-Authenticate: Bearer realm="acme"` |
| Malformed credential | `401` | `INVALID_CREDENTIALS` | `WWW-Authenticate` |
| Expired token | `401` | `TOKEN_EXPIRED` | `WWW-Authenticate: Bearer error="invalid_token"` |
| Revoked token | `401` | `TOKEN_REVOKED` | `WWW-Authenticate` |
| Valid credential, suspended account | `403` | `ACCOUNT_SUSPENDED` | — |

Design rules:

- **`401` means identity; never use it for permission problems.** An expired token is `401`
  (refresh may fix it); a valid user touching another tenant is `403` or `404`.
- **Always send `WWW-Authenticate`** on `401` per RFC 9110; clients and SDKs use it to decide
  whether to refresh.
- **Do not reveal which part failed beyond the minimum.** "Token expired" is useful to a
  legitimate client and low-risk; "signature mismatch on key 3" is reconnaissance. Keep messages
  coarse where they enable enumeration.
- **Attach the principal to a request-scoped context**, never a module-level variable. Concurrent
  requests under a global variable is a data-leak class of bug.
- **Errors from the identity provider are not the same as invalid credentials.** An IdP outage
  should be `503` (`AUTH_PROVIDER_UNAVAILABLE`), not `401` — otherwise every user is told their
  token is bad during an outage.

```ts
function authenticate(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header?.startsWith("Bearer ")) {
    return next(new AuthError("TOKEN_MISSING"));   // registry: 401 + WWW-Authenticate
  }
  try {
    req.principal = verifyToken(header.slice(7));   // throws TokenExpired, etc.
    next();
  } catch (err) {
    next(toAuthError(err));                          // IdP outage → 503, not 401
  }
}
```

## 21.4 — Authorization middleware

Authorization checks the resolved principal against the action and resource: role checks,
ownership, tenant isolation, entitlement.

| Condition | Status | Why |
| --------- | ------ | --- |
| Authenticated, lacks role/permission | `403` | Known identity, refused |
| Cross-tenant resource access | `404` (recommended) or `403` | `404` avoids confirming existence |
| Resource exists but is another user's private data | `404` | Same hiding rule |
| Feature not in the plan (entitlement) | `403` or `402`/`409` by policy | Document; `403` is the common default |
| Principal is a valid service with insufficient scope | `403` | Not a credential problem |

Rules:

- **Existence hiding is a policy decision, applied consistently.** If a caller may not know a
  resource exists, return `404` — even though the true reason is permission. Inconsistent
  `403`-vs-`404` across endpoints becomes an enumeration oracle.
- **Never let authz depend on unvalidated body fields.** Authorize against parsed and (where
  relevant) validated data; otherwise a type-confusion can bypass a check.
- **Check tenant scope on every query**, not just at the endpoint. Row-level filtering is the
  backstop for a missed check (Ch. 35).
- **`403` responses should not enumerate what the caller *would* need.** "Requires the editor
  role" is acceptable when roles are public; listing internal permission IDs is not.
- **Audit denials.** Every `403`/`404`-by-hiding on a sensitive resource should be logged with
  the principal and `requestId` for security review.

```ts
function authorize(action: Action) {
  return (req: Request, res: Response, next: NextFunction) => {
    const principal = req.principal!;
    if (!principal.can(action, req.params)) {
      // Policy: hide existence of other tenants' resources.
      const hides = action.tenantScoped;
      return next(new AuthzError(hides ? "RESOURCE_NOT_FOUND" : "INSUFFICIENT_ROLE"));
    }
    next();
  };
}
```

## 21.5 — Rate-limit middleware

Rate limiting rejects a caller whose request rate or quota is exceeded. It belongs close to the
front of the chain but **after authentication when the key is the principal**.

| Key | Runs | Pros | Cons |
| --- | ---- | ---- | ---- |
| IP address | Before auth | Cheap; sheds unauthenticated floods | Shared NAT; defeated by distributed clients |
| API key / principal | After auth | Fair per tenant; hard to evade | Requires auth first |
| Tenant | After auth | Protects against one tenant starving others | Needs tenant context |
| Endpoint + principal | After auth | Protects expensive operations specifically | More state |

Rules:

- **Always send `Retry-After`** with `429`; the value should reflect the limiter's window.
- **Include limit metadata** in the body via an extension (`retryAfterSeconds`) and, commonly,
  `RateLimit`/`RateLimit-Policy` style headers where supported.
- **Classify quota vs rate.** A short-term rate limit is `429`; a hard plan quota (e.g. "10k
  exports/month") may be `429` with a distinct code like `QUOTA_EXCEEDED`, or `403` if it is an
  entitlement. Pick one and document it.
- **Use token buckets or sliding windows; avoid fixed windows** that allow a double burst at the
  boundary.
- **Fail safe on limiter failure.** If the rate-limit store (Redis) is down, decide explicitly:
  fail open (allow, log, alert) or fail closed (reject). For protecting a fragile backend, fail
  closed with `503`; for protecting a non-critical endpoint, fail open. Never leave it implicit.

```ts
function rateLimit(key: (req: Request) => string, limit: number, windowSec: number) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { allowed, retryAfter } = await bucket(key(req), limit, windowSec);
      if (!allowed) {
        res.set("Retry-After", String(retryAfter));
        return next(new RateLimitError(retryAfter));   // registry: 429
      }
      next();
    } catch {
      // Limiter store unavailable: fail closed for a protected backend.
      next(new ServiceUnavailableError("RATE_LIMITER_UNAVAILABLE"));
    }
  };
}
```

## How it works — ordering the three

```text
path/method routable?
   no → 404/405
   yes ↓
size/content-type ok?
   no → 413/415
   yes ↓
parse body (if body present)
   fail → 400
   ok ↓
AUTHENTICATE            fail → 401 (+ WWW-Authenticate)
   ok ↓
AUTHORIZE               fail → 403 / 404 (hiding) / 402 by policy
   ok ↓
RATE LIMIT (per identity) fail → 429 (+ Retry-After)
   ok ↓
handler
```

The one thing to remember: **a limit keyed on identity cannot run before identity is known.**

## Worked example — Acme SaaS AgentRun

`POST /api/v1/agent/runs` is expensive. Acme stacks the guards:

1. **Size + type:** JSON only, ≤ 256 KiB → `415`/`413` before parsing.
2. **Parse:** bad JSON → `400`.
3. **Auth:** missing/expired token → `401` with `WWW-Authenticate`.
4. **Authz:** caller lacks the `editor` role to run agents → `403` `INSUFFICIENT_ROLE`.
5. **Rate limit per tenant:** over the run budget → `429` with `Retry-After: 60` and
   `retryAfterSeconds: 60`.

```http
HTTP/1.1 429 Too Many Requests
WWW-Authenticate: (not present)
Retry-After: 60
Content-Type: application/problem+json
X-Request-Id: req_r3

{
  "type": "/problems/rate-limited", "title": "Too Many Requests",
  "status": 429, "detail": "Agent runs are limited to 20 per minute per workspace.",
  "instance": "/api/v1/agent/runs", "code": "RATE_LIMITED",
  "requestId": "req_r3", "retryAfterSeconds": 60
}
```

The key is the *tenant*, not the IP, so a noisy tenant is throttled without penalizing anyone
behind the same NAT — and the limit runs after auth because the tenant is not known until then.

## Key data / numbers

- **`401`** requires `WWW-Authenticate`; bearer error codes include `invalid_token` and
  `insufficient_scope` (the latter is a `403`-flavored condition carried on a `401` challenge in
  OAuth flows — keep your REST API's `403` for authorization to avoid confusion).
- **`403`** for authenticated-but-forbidden; **`404`** as the hiding alternative.
- **`429`** requires `Retry-After`; delta-seconds or HTTP-date.
- **RateLimit headers** (IETF RateLimit fields) and `Retry-After` give clients machine guidance;
  mirror the delay in the body as `retryAfterSeconds`.
- **Token buckets** are the common algorithm; fixed windows allow up to 2× burst at boundaries.
- **IdP outage** during auth → `503`, not `401`.

## Real-world use case — Acme SaaS tenant fairness

Acme originally rate-limited `Checkout` and `AgentRun` by IP before authentication. A large
customer behind a corporate NAT began exceeding the shared IP limit, so *all* of that customer's
users were throttled while a scripted attacker rotating IPs was never limited at all. The team
moved the limit after authentication, keyed on `tenantId`, with a small pre-auth IP limit for
anonymous endpoints only. Fairness improved immediately, the attacker's rotation stopped helping,
and support tickets tagged "unfair rate limit" dropped to near zero. The change was purely
ordering and key selection — no new infrastructure.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| IP limit before auth | Cheap; protects the auth path itself | NAT unfairness; evadable | Anonymous/edge shields only |
| Identity limit after auth | Fair; hard to evade | Auth cost paid before rejection | Default for authenticated APIs |
| `403` for cross-tenant access | Honest about permission | Confirms resource existence | When existence is not sensitive |
| `404` for cross-tenant access | Hides existence | Slightly more confusing to debug | Multi-tenant SaaS default |
| Limiter fails closed | Protects fragile backends | Rejects during store outage | Critical/expensive endpoints |
| Limiter fails open | Availability during outage | Risk of overload | Non-critical endpoints |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `401` for identity, `403` for permission, `429` for quota | Mix them up |
| Send `WWW-Authenticate` on `401`, `Retry-After` on `429` | Return bare status codes |
| Key identity limits on the principal/tenant | Key authenticated limits on IP |
| Apply hiding policy consistently (`404`) | Alternate `403`/`404` for the same resource class |
| Map IdP outages to `503` | Tell users their token is invalid during an outage |
| Attach the principal to request scope | Store the principal in a module variable |

## Common mistakes

- **Authz before parse when the decision needs the body.** Authorizing against `undefined` fields
  is both wrong and a bypass vector.
- **Rate limiting before auth on an authenticated API.** You key on the wrong thing and pay the
  attacker's spoofed IPs.
- **`401` with no `WWW-Authenticate`.** Clients cannot decide whether to refresh.
- **Enumerating permissions in `403` detail.** Reveals internal authorization structure.
- **Implicit limiter-failure behavior.** An unhandled Redis error becomes a `500` storm; decide
  fail-open vs fail-closed on purpose.

## Checklist

- [ ] Order is size/type → parse → auth → authz → rate limit → handler.
- [ ] `401` always carries `WWW-Authenticate`; `429` always carries `Retry-After`.
- [ ] Identity-keyed limits run after authentication.
- [ ] Existence-hiding policy is applied consistently across endpoints.
- [ ] IdP/limiter outages map to `503`, not `401`/`403`.
- [ ] Principal and tenant are request-scoped, never global.

## Related

- [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)
- [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)
- [Authentication, Authorization, and Tenant Isolation Errors (Ch. 35)](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
