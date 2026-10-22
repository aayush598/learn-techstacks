# Practical — Consistent 401 vs 403 Middleware

> Part XIII · Chapter 35 · Sections 35.1–35.5, 35.11 · _Estimated reading time: 20 min_
> **Prerequisite:** [Deep Dive: Consistent 401 vs 403](../02-deep-dive/01-consistent-401-vs-403.md)

## In one sentence

This file implements the **complete auth/authz middleware stack** — parse, authenticate, resolve
visibility, authorize — where every outcome is one of four fixed responses (`401`, `uniform 404`,
`403`, `403 insufficient_scope`), so no endpoint can leak existence or leak token state.

## Why this matters in production

Handlers drift. Given the freedom, one developer returns `403` where another returns `404`, and the
API develops an enumeration oracle endpoint by endpoint. A shared stack removes the freedom: the
status is decided in one reviewed place, every handler inherits it, and a CI test asserts the
contract. This is the executable form of the chapter's rules.

## The stack (four stages)

```text
     ┌──────────┐   ┌──────────────┐   ┌────────────────┐   ┌──────────────┐
 ──▶ │ parse    │──▶│ authenticate │──▶│ resolve        │──▶│ authorize    │──▶ handler
     │ token    │   │ → principal  │   │ visibility     │   │ → allow/deny │
     └──────────┘   └──────────────┘   └────────────────┘   └──────────────┘
        no token       invalid           hidden/missing        no role/scope
        → 401          → 401             → 404                 → 403
```

## Step 1 — Authentication middleware

```ts
import { verifyAccessToken } from "./tokens";

export async function authenticate(req: Request, res: Response, next: NextFunction) {
  const header = req.header("authorization");

  // Missing credentials: 401 with a challenge.
  if (!header || !header.startsWith("Bearer ")) {
    return unauthorized(res);
  }

  const token = header.slice("Bearer ".length).trim();
  const result = await verifyAccessToken(token); // -> { ok } | { ok:false, reason }

  if (!result.ok) {
    // Invalid/expired/revoked all return the SAME 401; reason is internal only.
    log.warn({ event: "auth_failed", requestId: req.id, reason: result.reason }, "auth failed");
    metrics.increment("auth_failed_total", { reason: result.reason });
    return unauthorized(res);
  }

  req.principal = result.principal;
  next();
}

function unauthorized(res: Response) {
  res.setHeader("WWW-Authenticate", 'Bearer realm="api", error="invalid_token"');
  return res.status(401).json({ code: "UNAUTHENTICATED", message: "Authentication required." });
}
```

## Step 2 — Visibility resolution

```ts
type Loader = (req: Request) => Promise<{ resource: Resource | null }>;

// Loads the resource and decides visibility in ONE place.
export function resolveVisible(load: Loader) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { resource } = await load(req);
      const principal = req.principal!;

      // Merge "missing" and "not visible" into a single outcome.
      const visible = resource !== null && resource.tenantId === principal.tenantId;
      if (!visible) return res.status(404).json({ code: "NOT_FOUND", message: "Not found." });

      req.resource = resource;
      next();
    } catch (e) {
      // A load error must never confirm existence.
      next(e);
    }
  };
}
```

## Step 3 — Authorization middleware

```ts
export function authorize(action: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const principal = req.principal!;
    const resource = req.resource;

    // Bearer scope check (RFC 6750): authenticated but missing scope -> 403.
    const requiredScope = scopeFor(action);
    if (requiredScope && !principal.scopes.includes(requiredScope)) {
      res.setHeader(
        "WWW-Authenticate",
        `Bearer realm="api", error="insufficient_scope", scope="${requiredScope}"`,
      );
      return res.status(403).json({ code: "INSUFFICIENT_SCOPE", message: "Insufficient scope." });
    }

    let allowed = false;
    try {
      allowed = policyCan(principal, action, resource); // sync/async policy
    } catch (e) {
      metrics.increment("authz_check_error_total"); // page
      log.error({ event: "authz_check_failed", requestId: req.id }, "policy engine error");
      return res.status(403).json({ code: "FORBIDDEN", message: "You do not have access." });
    }

    if (!allowed) {
      // Existence is already known here, so 403 is safe.
      return res.status(403).json({ code: "FORBIDDEN", message: "You do not have access." });
    }
    next();
  };
}
```

## Step 4 — Compose per route

```ts
router.get(
  "/projects/:id",
  authenticate,                                   // 401 on missing/invalid
  resolveVisible((req) => projects.findById(req.params.id)), // 404 on hidden/missing
  authorize("project:read"),                      // 403 on denial
  (req, res) => res.json(projectDto(req.resource!)),
);
```

The handler **never** sets an access status — it only runs when all checks passed.

## The four responses, in one table

| Stage | Condition | Status | Body | Header |
| ----- | --------- | ------ | ---- | ------ |
| authenticate | no/invalid/expired/revoked token | `401` | `{code:"UNAUTHENTICATED"}` | `WWW-Authenticate: invalid_token` |
| resolveVisible | missing OR other-tenant | `404` | `{code:"NOT_FOUND"}` | — |
| authorize | role denied, existence known | `403` | `{code:"FORBIDDEN"}` | — |
| authorize | Bearer scope missing | `403` | `{code:"INSUFFICIENT_SCOPE"}` | `WWW-Authenticate: insufficient_scope` |

## Testing the stack

```ts
test("access contract holds for projects", async () => {
  const a = await tokenFor("tenant_a", { role: "member" });
  const bProj = await createProject("tenant_b");
  const aProj = await createProject("tenant_a");

  const foreign = await get(`/projects/${bProj.id}`, a);
  const missing = await get(`/projects/${uuid()}`, a);
  expect(foreign.status).toBe(404);
  expect(foreign.body).toEqual(missing.body);          // byte-identical

  const noScope = await get(`/projects/${aProj.id}`, tokenWithScopes([]));
  expect(noScope.status).toBe(403);
  expect(noScope.headers["www-authenticate"]).toContain("insufficient_scope");
});
```

## Key data / numbers

- **RFC 9110** §15.5.2/§15.5.4 for `401`/`403`; **RFC 6750** for `insufficient_scope` → `403`.
- **OWASP A01/A07**; **CWE-204/CWE-639/CWE-863**.
- **Invariant**: handler executes only after `authenticate → resolveVisible → authorize` pass.
- **Alarm**: non-zero `authz_check_error_total` pages; `auth_failed_total{reason}` is a bounded metric.

## Real-world use case — Acme SaaS

Acme replaced per-handler auth with this four-stage stack across its REST API. The migration surfaced
three endpoints that had returned `403` for cross-tenant resources; the shared `resolveVisible` merged
them into the uniform `404`. The test above — foreign vs missing byte-identical — is now mandatory for
every new resource route; a route without the test fails review. Time-to-add a secured endpoint
dropped because handlers became trivial, and the access contract stopped drifting.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Four-stage middleware stack | Consistent, testable | Requires route composition | All REST resources |
| Per-handler checks | Flexible | Drifts, leaks | Never for shared APIs |
| `404` everywhere for denial | Maximal hiding | Worse collaborator UX | Private-existence resources |

## Common mistakes

- **Handler that overrides access status.** Reintroduces drift.
- **Visibility after authorization.** Leaks existence.
- **`500` on a policy error.** Should deny (`403`) and alarm.
- **Different 404 bodies for foreign vs missing.** The oracle persists.
- **Skipping the scope check.** Returns `403 FORBIDDEN` where `insufficient_scope` is correct.

## Checklist

- [ ] Are all routes composed from the four shared stages?
- [ ] Does any handler set an access status itself?
- [ ] Are foreign and missing resources byte-identical?
- [ ] Do Bearer scope failures use `insufficient_scope`?
- [ ] Is `authz_check_error_total` alarmed?
- [ ] Is there a CI access-contract test per resource type?

## Related

- [Consistent 401 vs 403](../02-deep-dive/01-consistent-401-vs-403.md)
- [Missing and Invalid Credentials](../01-concepts/01-missing-and-invalid-credentials.md)
- [Practical: Tenant Isolation Check](./02-tenant-isolation-check.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
