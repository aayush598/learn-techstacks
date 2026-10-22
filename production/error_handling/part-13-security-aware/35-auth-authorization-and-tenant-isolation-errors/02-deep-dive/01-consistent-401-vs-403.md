# Deep Dive — Consistent 401 vs 403

> Part XIII · Chapter 35 · Sections 35.10–35.12 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Existence Disclosure and Consistent Status](../01-concepts/05-existence-disclosure-and-consistent-status.md)

## In one sentence

A consistent 401/403/404 policy is a **single decision function** that runs in one place, evaluates
"authenticated? → visible? → permitted?" in that fixed order, emits one of four outcomes, and
**fails closed** when any check throws — so no endpoint can invent its own status and leak existence.

## Why this matters in production

Status codes are a language. When different endpoints speak it differently, attackers read the
inconsistency as an oracle. The only robust fix is architectural: extract the decision into shared
middleware so that "which status" is answered once, tested once, and impossible to get wrong per
handler. This file gives the exact decision tree, the middleware mechanics, and the failure behavior.

## The decision tree

```text
                ┌────────────────────────────────┐
   request ────▶│ authenticated?                  │
                └───────────────┬────────────────┘
                    no          │        yes
             ┌──────────────────┘         │
             ▼                            ▼
        401 UNAUTHENTICATED     ┌──────────────────────────────┐
        (+ WWW-Authenticate)    │ resource resolvable &         │
                                │ visible to this caller?       │
                                └───────────┬──────────────────┘
                                    no      │      yes
                        ┌───────────────────┘        │
                        ▼                            ▼
                404 NOT_FOUND          ┌───────────────────────────┐
        (uniform: missing OR hidden)   │ permitted (role/scope)?    │
                                       └───────────┬───────────────┘
                                           no      │      yes
                              ┌────────────────────┘        │
                              ▼                             ▼
                    403 FORBIDDEN (or            proceed to handler
                    insufficient_scope)                 │
                                                        ▼
                                              (handler may still
                                               return 404 for a
                                               genuinely absent id)
```

Two invariants:

1. **Order is fixed**: authenticated → visible → permitted. Never check permission before visibility.
2. **The 404 branch merges two causes**: nonexistent *and* exists-but-hidden produce the identical
   response.

## Middleware mechanics

```ts
type Principal = { id: string; tenantId: string; role: string; scopes: string[] };

// One place that answers "which status" for the whole API.
function authorize(
  resolve: (req: Request) => Promise<Resource | null>, // loads resource + visibility
  action: string,
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const principal = req.principal; // set by the auth middleware
    if (!principal) {
      res.setHeader("WWW-Authenticate", 'Bearer realm="api", error="invalid_token"');
      return res.status(401).json({ code: "UNAUTHENTICATED" });
    }

    let resource: Resource | null;
    try {
      resource = await resolve(req);
    } catch (e) {
      // A load error must not become an allow; treat as hidden/absent.
      next(accessError(e));
      return;
    }

    // Visibility: consolidate "missing" and "not visible to this caller".
    const visible = resource !== null && resource.tenantId === principal.tenantId;
    if (!visible) return next(new NotFoundError("NOT_FOUND"));

    // Permission: only reached when existence is already known.
    let allowed: boolean;
    try {
      allowed = policyCan(principal, action, resource!);
    } catch (e) {
      // Fail closed on any check error, and alarm.
      metrics.increment("authz_check_error_total");
      return next(new ForbiddenError("FORBIDDEN"));
    }
    if (!allowed) return next(new ForbiddenError("FORBIDDEN"));

    next();
  };
}
```

Everything routes through `authorize`; handlers never set 401/403/404 themselves.

## RFC 6750 `insufficient_scope`

For Bearer tokens, a valid token missing a scope is the bearer-specific 403:

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer realm="api", error="insufficient_scope", scope="exports:read"
Content-Type: application/problem+json

{ "type": "about:blank", "title": "Insufficient scope", "status": 403 }
```

The caller is authenticated and the resource is theirs to know about, so `403` (not `404`) is correct
here — existence is not secret within their own scope.

## Fail-closed failure behavior

| Failure | Outcome | Why |
| ------- | ------- | --- |
| Principal missing | `401` | Not authenticated |
| Resource load throws | `404` (or `500`) | Never allow; do not confirm existence |
| Policy check throws | `403` + alarm | Deny, do not leak |
| Tenant context missing | `403`/`500` internally | Fail closed |
| IdP unreachable | `503` | Cannot verify; do not accept |

The rule that ties them together: **an error in the access path is a denial, not a pass.**

## Testing the contract

```ts
describe("access contract", () => {
  it("hidden and missing resources are byte-identical", async () => {
    const hidden = await get("/projects/other-tenant-id"); // exists, not visible
    const missing = await get("/projects/does-not-exist");
    expect(hidden.status).toBe(404);
    expect(missing.status).toBe(404);
    expect(hidden.body).toEqual(missing.body); // same code, same message, same shape
  });

  it("policy-engine error denies", async () => {
    policyCan.mockImplementation(() => { throw new Error("engine down"); });
    const res = await get("/projects/own-id");
    expect(res.status).toBe(403);
  });
});
```

The byte-identical assertion is the one that catches existence oracles in CI.

## Key data / numbers

- **RFC 9110** §15.5.2 (`401`, requires `WWW-Authenticate`) and §15.5.4 (`403`).
- **RFC 6750** maps `insufficient_scope` → `403` and invalid/missing token → `401`.
- **OWASP A01** and **CWE-204/CWE-639** describe the inconsistency and IDOR vectors this prevents.
- **Order rule**: authenticated → visible → permitted; reversing the first two leaks existence.

## Real-world use case — Acme SaaS

Acme had authorization scattered across 60 handlers. Two returned `403` for cross-tenant resources
while the rest returned `404`. A bug-bounty report used those two endpoints to confirm which workspace
ids existed. Fix: the `authorize` middleware above replaced all per-handler checks; a test suite now
asserts hidden-vs-missing byte-identical responses for every resource type; `authz_check_error_total`
pages on policy-engine errors. The two inconsistent endpoints were the entire finding, and the shared
middleware removed the class of bug.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared `authorize` middleware | One contract, testable | Requires a resource res. hook | Default |
| Per-handler authz | Local control | Inconsistent, leak-prone | Never in multi-tenant APIs |
| `404` for all denials | Maximal hiding | Worse collaborator UX | Private-existence resources |

## Common mistakes

- **Permission before visibility.** Leaks existence.
- **`500` for a policy-engine error.** Should deny (`403`) and alarm.
- **Handler that overrides the middleware status.** Reintroduces inconsistency.
- **Different 404 bodies/timing for hidden vs missing.** The oracle persists.
- **`401` for a scope failure.** Should be `403 insufficient_scope`.

## Checklist

- [ ] Is there exactly one authorization decision function?
- [ ] Is the order authenticated → visible → permitted enforced?
- [ ] Are hidden and missing resources byte-identical?
- [ ] Does any access-path error deny rather than allow?
- [ ] Is `authz_check_error_total` alarmed?
- [ ] Do Bearer scope failures return `403 insufficient_scope`?

## Related

- [Existence Disclosure and Consistent Status](../01-concepts/05-existence-disclosure-and-consistent-status.md)
- [Tenant Isolation Enforcement](./02-tenant-isolation-enforcement.md)
- [Practical: Consistent 401 vs 403](../03-practical-examples/01-consistent-401-vs-403.md)
- [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Glossary](../../../GLOSSARY.md)
