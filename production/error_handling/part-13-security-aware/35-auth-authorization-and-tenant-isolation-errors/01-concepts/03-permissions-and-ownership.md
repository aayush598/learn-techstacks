# Permissions and Ownership

> Part XIII · Chapter 35 · Sections 35.5–35.6 · _Estimated reading time: 16 min_
> **Prerequisite:** [Missing and Invalid Credentials](./01-missing-and-invalid-credentials.md)

## In one sentence

**Insufficient permissions** (the caller knows the resource exists but lacks the role) warrant a
`403`, while **ownership violations** and cases where existence itself is sensitive warrant a
`404` — because a `403` for a resource the caller cannot see *confirms that the resource exists*.

## Why this matters in production

Authorization is not one check; it is two questions answered in order: **"may this caller know this
resource exists?"** and **"may this caller act on it?"**. Collapsing them into a single `403`
publishes your inventory: an attacker enumerates workspace ids, project ids, and document ids and
learns which are real (those that return `403`) versus nonexistent (those that return `404`). The same
error that is polite for a known collaborator is a leak for an arbitrary authenticated user.

## Core concept — two questions, three answers

| Caller state | Existence | Action allowed | Response |
| ------------ | --------- | -------------- | -------- |
| Authenticated, may know it exists, lacks role | known | no | `403 FORBIDDEN` |
| Authenticated, may **not** know it exists | hidden | no | `404 NOT_FOUND` |
| Authenticated, is the owner, action allowed | known | yes | proceed |
| Not authenticated | — | — | `401` (see previous files) |

The **existence question always comes first**. If the caller may not know the resource exists, they
get the not-found outcome — the same one a truly nonexistent resource gets.

## The existence rule

```text
                  ┌──────────────────────────────────────┐
   request ──────▶│ resolve resource by id                │
                  └───────────────┬──────────────────────┘
                                  │
              ┌───────────────────┼───────────────────────┐
              ▼                   ▼                       ▼
        does not exist      exists, caller           exists, caller
                            may NOT see it            may see it
              │                   │                       │
              └────────┬──────────┘                       ▼
                       ▼                          ┌──────────────────┐
                  uniform 404                     │ role check       │
                                                  ├─ role ok ─▶ allow │
                                                  └─ role no ─▶ 403   │
                                                  └──────────────────┘
```

Notice: **the code path for "does not exist" and "exists but invisible" must be the same** — same
status, body, and timing — or the distinction is observable even with identical status codes.

## Worked example — ownership vs role

```ts
// ❌ Confirms existence to anyone: 403 for a resource they may not see.
async function getProject(projectId: string, principal: Principal) {
  const project = await projects.findById(projectId);
  if (!project) throw new NotFoundError("PROJECT_NOT_FOUND");     // 404
  if (project.tenantId !== principal.tenantId)
    throw new ForbiddenError("PROJECT_FORBIDDEN");                 // 403 ← leaks existence
  if (!principal.can("project:read", project))
    throw new ForbiddenError("PROJECT_FORBIDDEN");                 // 403 (legit)
  return project;
}

// ✅ Existence question first: invisible and nonexistent share one outcome.
async function getProject(projectId: string, principal: Principal) {
  const project = await projects.findById(projectId);

  // A caller may only learn of projects in their own tenant.
  const visible = project !== null && project.tenantId === principal.tenantId;
  if (!visible) throw new NotFoundError("NOT_FOUND");              // 404 for both miss & foreign

  if (!principal.can("project:read", project))
    throw new ForbiddenError("FORBIDDEN");                          // 403 only when existence is known
  return project;
}
```

The rewritten `visible` check collapses "missing" and "other tenant" into one branch — the correct
design, and the one the tenant-isolation guard in
[the practical example](../03-practical-examples/02-tenant-isolation-check.md) enforces.

## Permission model mechanics

| Model | Typical error | Notes |
| ----- | ------------- | ----- |
| RBAC (role → permission) | `403 FORBIDDEN` | Caller may see resource; role too low |
| Ownership check | `404` (hide) or `403` (own domain) | Depends on whether existence is sensitive |
| ACL per resource | `404` if caller not in ACL **and** existence is private | Otherwise `403` |
| ABAC/policy (attributes) | `403` for known resources | Policy engine decides; fail closed |
| Scope check (OAuth `scope`) | `403 insufficient_scope` | See RFC 6750 |

### RFC 6750 `insufficient_scope`

For Bearer tokens, a valid token lacking the required scope is the one "403-like" case the bearer
spec names explicitly. Return `403` with
`WWW-Authenticate: Bearer error="insufficient_scope"` — the caller is authenticated and the resource
is theirs to know about.

## Key data / numbers

- **RFC 9110 §15.5.4**: `403 Forbidden` — the server understood the request but refuses to
  authorize it; the resource may exist.
- **RFC 6750**: `insufficient_scope` → `403`; `invalid_token` → `401`.
- **OWASP A01: Broken Access Control** is the #1 risk; existence disclosure via `403` is a documented
  enumeration vector.
- **CWE-204** (observable response discrepancy) and **CWE-639** (authorization bypass through
  user-controlled key).
- **Rule of thumb**: default to `404` for cross-tenant and any resource whose existence is private;
  use `403` only inside a domain the caller legitimately shares.

## Real-world use case — Acme SaaS

Acme's project API returned `403` for projects in another tenant and `404` for nonexistent ones. A
competitor enumerated Acme's enterprise customers by probing sequential project ids and counting
`403`s versus `404`s — effectively a customer list. Fix: the project repository now resolves visibility
(a project is visible only within the caller's tenant), and invisible/absent both return a uniform
`404 NOT_FOUND`; only a same-tenant role failure returns `403`. The enumeration technique now yields
no signal, and the same guard is applied to documents, comments, and attachments.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `404` for foreign/hidden resources | No existence leak | Slightly harder UX for collaborators | Default for private existence |
| `403` for all denials | Simple, explicit | Leaks existence | Only when existence is public |
| `403` inside shared domain, `404` outside | Precise and safe | Requires a visibility model | Multi-tenant default |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "may they know it exists?" first | Return `403` to anyone denied |
| Make invisible and absent byte-identical | Different messages for miss vs foreign |
| Use `403` only within a shared domain | Use `403` for cross-tenant resources |
| Use `insufficient_scope` for Bearer scope | Return `401` for a scope failure |
| Keep timing uniform between the two 404s | Return early only for the missing case |

## Common mistakes

- **`403` for cross-tenant access.** The #1 existence-disclosure bug in multi-tenant APIs.
- **Different messages for miss vs foreign.** Even with `404`, text leaks.
- **Different timing for miss vs foreign.** The foreign path may do an extra authz call.
- **Returning `401` for a scope failure.** That is `403 insufficient_scope`.
- **Checking role before existence.** Order matters; existence first.

## Checklist

- [ ] Is existence resolved before permission is evaluated?
- [ ] Do invisible and absent resources return identical status + body + timing?
- [ ] Is `403` used only where the caller may know the resource exists?
- [ ] Do Bearer scope failures return `403 insufficient_scope`?
- [ ] Is the same visibility guard applied to every resource type?

## Related

- [Tenant Isolation and Context](./04-tenant-isolation-and-context.md)
- [Existence Disclosure and Consistent Status](./05-existence-disclosure-and-consistent-status.md)
- [Practical: Tenant Isolation Check](../03-practical-examples/02-tenant-isolation-check.md)
- [Chapter 18 — Domain and Business Logic Errors](../../../part-07-validation-and-business-errors/18-domain-and-business-logic-errors/README.md)
- [Glossary](../../../GLOSSARY.md)
