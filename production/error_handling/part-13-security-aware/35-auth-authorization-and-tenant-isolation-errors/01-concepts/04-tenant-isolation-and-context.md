# Tenant Isolation and Context

> Part XIII · Chapter 35 · Sections 35.7–35.9 · _Estimated reading time: 17 min_
> **Prerequisite:** [Permissions and Ownership](./03-permissions-and-ownership.md)

## In one sentence

**Cross-tenant access**, **tenant context failures**, and **suspension/entitlement** errors are the
failure modes that break a multi-tenant SaaS contract — cross-tenant access must be a non-event
(uniform `404`), missing tenant context must fail closed, and suspension errors must not leak another
tenant's data.

## Why this matters in production

Tenant isolation is the guarantee that one customer can never see or affect another's data. Error
handling is where that guarantee is most often broken, because:

- A query that forgets the `tenant_id` filter "succeeds" and returns another tenant's row — a breach,
  not an error.
- A failed tenant *context* (missing header, bad subdomain) leaves the query unscoped — the worst
  possible default.
- An entitlement/suspension error that names the plan or feature of another tenant leaks business
  information.

The recurring failure is not a missing check at one endpoint; it is a **missing default** — the
absence of a hard rule that every data access is tenant-scoped.

## Core concept — context, scope, enforcement

```text
   request
      │
      ▼
 resolve tenant context        <-- from JWT claim, session, subdomain, header (in that order)
      │  (must be explicit; never inferred from the resource id)
      ▼
 attach to request/scope       <-- tenantId travels with every DB call, cache key, job
      │
      ▼
 enforce at data layer         <-- WHERE tenant_id = :tid, RLS, or repository guard
      │
      ▼
 cross-tenant attempt ────────▶ uniform 404 (identical to not-found)
```

Three rules:

1. **Context is explicit and authoritative.** Tenant comes from the authenticated principal, never
   from a client-supplied resource id.
2. **Scope travels with the work.** Every DB query, cache read, queue message, and log line carries
   the tenant.
3. **Enforcement is at the data layer**, not only in the handler — defense in depth.

## Tenant context sources

| Source | Trust | Notes |
| ------ | ----- | ----- |
| JWT/ID-token claim (`tid`) | ✅ authoritative | Preferred; signed by the IdP |
| Session record | ✅ authoritative | Server-side, trusted |
| Subdomain (`acme.app.com`) | ⚠️ verify against principal | Must match the principal's tenant |
| Request header (`X-Tenant-Id`) | ❌ never trust alone | Must be validated against the principal |
| Resource id/path | ❌ never use as context | That is the thing you must scope |

> ⚠️ **Hazard.** Taking the tenant from a client header or subdomain *without* cross-checking the
> authenticated principal is a classic IDOR: the attacker sets `X-Tenant-Id: victim` and reads
> victim data.

## Tenant context failure

When context cannot be resolved (no claim, header/claim mismatch, deleted tenant):

| Case | Response | Rationale |
| ---- | -------- | --------- |
| No tenant claim at all | `401` or `403` | Cannot authenticate/authorize |
| Header/mismatch vs principal | `403` (or uniform `404`) | Attempted to act as another tenant |
| Deleted tenant | `401` | Principal no longer valid |
| Missing context on internal call | **fail closed** (`500` internally, deny) | Never run unscoped |

**The dangerous default is "no tenant means all tenants".** A missing scope must never widen access.

## Suspension and entitlement errors

```ts
// ❌ Reveals plan/feature details; may leak another tenant's locked state.
if (tenant.suspended) throw new ForbiddenError(`Account suspended, plan=${tenant.plan}`);

// ✅ Stable, non-revealing code; details stay internal.
if (tenant.suspended) {
  throw new PermissionError("TENANT_SUSPENDED", "This workspace is not available.", {
    httpStatus: 403,
    internal: { tenantId: tenant.id, plan: tenant.plan, reason: tenant.suspendReason },
  });
}
if (!tenant.hasEntitlement(feature)) {
  throw new PermissionError("FEATURE_NOT_INCLUDED", "This feature is not available on your plan.");
}
```

Suspension should be `403` (the tenant exists and the caller belongs to it); the caller is entitled
to know *their own* workspace is suspended, but not the suspension reason if it is investigative, and
never another tenant's state.

## Enforcing with defense in depth

```ts
// Repository guard: every query must supply a scope, or it throws internally.
class ScopedRepository<T> {
  constructor(private scope: TenantScope) {}

  async findById(id: string): Promise<T | null> {
    if (!this.scope.tenantId) throw new InternalError("MISSING_TENANT_SCOPE"); // fail closed
    return db.one<T>(
      "SELECT * FROM items WHERE id = $1 AND tenant_id = $2", // parameterized + scoped
      [id, this.scope.tenantId],
    );
  }
}
```

```sql
-- Optional second layer: PostgreSQL Row-Level Security, fail closed by default.
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON items
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- If app.tenant_id is unset, current_setting throws -> query errors -> no rows leak.
```

The DB layer is the last line: even if application code forgets the filter, RLS denies by default.

## Key data / numbers

- **OWASP A01: Broken Access Control** — IDOR and cross-tenant access are its core; **A04: Insecure
  Design** covers missing tenant scoping.
- **CWE-639** (authorization bypass through user-controlled key), **CWE-566** (access control bypass
  by user-controlled SQL key).
- **PostgreSQL RLS**: `current_setting('app.tenant_id')` with no default raises an error — a
  fail-closed default; set it per transaction/connection.
- **Cache keys**: always `t:{tenantId}:...`; a shared key across tenants is a cross-tenant read.
- **`403` vs `401`**: a header/principal mismatch is an authorization problem (`403`) or, when
  existence is private, a uniform `404`.

## Real-world use case — Acme SaaS

Acme's `ExportJob` built an S3 object key as `exports/{exportId}.csv`. Two tenants could collide on
an `exportId` (generated by a buggy client), and the download endpoint resolved objects by key alone,
so tenant B's download returned tenant A's data — a full cross-tenant breach discovered in a security
review. Fix: object keys became `t/{tenantId}/exports/{exportId}.csv`, the download handler resolves
visibility (tenant must match) and returns a uniform `404` on mismatch, the `exportId` is a
server-generated UUID, and an RLS policy on the exports table enforces the tenant filter at the
database. Automated cross-tenant tests now run against every resource type on each build.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| App-layer scoping only | Simple, portable | One missed filter = breach | Small apps, with tests |
| App-layer + DB RLS | Defense in depth | DB-specific, per-connection setup | Multi-tenant production |
| Tenant-per-schema/database | Strong isolation | Operational overhead | High-assurance / regulated |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive tenant from the principal | Trust `X-Tenant-Id` alone |
| Fail closed on missing scope | Treat "no tenant" as "all tenants" |
| Scope every query, cache key, and job | Assume the handler added the filter |
| Return uniform `404` for cross-tenant | Return a distinguishing `403` |
| Keep suspension reasons internal | Name another tenant's plan/state |

## Common mistakes

- **Tenant from a client header.** IDOR.
- **Missing scope widening access.** The worst default.
- **Forgetting cache and object keys.** Data leaks outside the DB.
- **Inconsistent visibility guards.** One unscoped endpoint is the whole breach.
- **Verbose suspension errors.** Leak plan/feature/incident detail.

## Checklist

- [ ] Is the tenant always derived from the authenticated principal?
- [ ] Does missing context fail **closed** everywhere?
- [ ] Are all DB queries, cache keys, object keys, and jobs tenant-scoped?
- [ ] Is there a DB-level backstop (RLS / tenant-per-schema)?
- [ ] Does cross-tenant access return a uniform `404`?
- [ ] Are suspension/entitlement errors non-revealing?

## Related

- [Permissions and Ownership](./03-permissions-and-ownership.md)
- [Existence Disclosure and Consistent Status](./05-existence-disclosure-and-consistent-status.md)
- [Deep dive: Tenant Isolation Enforcement](../02-deep-dive/02-tenant-isolation-enforcement.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Glossary](../../../GLOSSARY.md)
