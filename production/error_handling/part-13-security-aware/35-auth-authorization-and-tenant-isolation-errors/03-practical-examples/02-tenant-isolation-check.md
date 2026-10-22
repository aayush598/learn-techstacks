# Practical — Tenant Isolation Check

> Part XIII · Chapter 35 · Sections 35.6–35.8, 35.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [Deep Dive: Tenant Isolation Enforcement](../02-deep-dive/02-tenant-isolation-enforcement.md)

## In one sentence

This file builds a **tenant-scoping guard** — a repository/ORM layer that refuses to run without a
tenant scope, applies the tenant filter to every operation, and turns any cross-tenant or unscoped
attempt into the **uniform 404** (or an internal fail-closed error), with a DB policy as backstop.

## Why this matters in production

Tenant isolation fails through *omission*: a new query, a cache read, an object download that forgets
the tenant dimension. You cannot rely on remembering. The guard makes the tenant a **required
parameter** of every data operation so that "forget the tenant" becomes a compile-time or
runtime error rather than a silent cross-tenant read.

## Design: scope is mandatory

```ts
type TenantScope = { tenantId: string; userId?: string; requestId: string };

class MissingTenantScopeError extends Error {
  code = "MISSING_TENANT_SCOPE";
}
```

A repository constructor requires a `TenantScope`; an empty `tenantId` throws immediately.

```ts
class ScopedRepo<T extends { id: string; tenantId: string }> {
  constructor(private db: Db, private table: string, private scope: TenantScope) {
    if (!scope?.tenantId) throw new MissingTenantScopeError("tenant scope required");
  }

  async findById(id: string): Promise<T | null> {
    return this.db.one<T>(
      `SELECT * FROM ${this.table} WHERE id = $1 AND tenant_id = $2`,
      [id, this.scope.tenantId],
    );
  }

  async list(limit = 50): Promise<T[]> {
    return this.db.many<T>(
      `SELECT * FROM ${this.table} WHERE tenant_id = $1 ORDER BY created_at DESC LIMIT $2`,
      [this.scope.tenantId, limit],
    );
  }

  async insert(row: Omit<T, "tenantId">): Promise<T> {
    // Writes force the tenant from scope; the client cannot set it.
    return this.db.one<T>(
      `INSERT INTO ${this.table} (id, tenant_id, ...) VALUES ($1, $2, ...) RETURNING *`,
      [row.id, this.scope.tenantId],
    );
  }
}
```

Note the `insert`: the tenant is taken **from the scope**, never from client input. A client-supplied
`tenantId` is ignored.

## The visibility guard (uniform 404)

```ts
async function getProjectVisible(scope: TenantScope, projectId: string) {
  const repo = new ScopedRepo<Project>(db, "projects", scope);
  const project = await repo.findById(projectId); // already tenant-filtered
  if (!project) throw new NotFoundError("NOT_FOUND"); // missing AND foreign share this
  return project;
}
```

Because `findById` filters by tenant, a foreign project returns `null` exactly like a missing one. The
handler throws one `NotFoundError`; the access layer maps it to the uniform `404`.

## Cross-layer composition

```text
   POST /projects/:id/archive
        │
        ▼
   authenticate ─────────────▶ principal (tenantId, role)
        │
        ▼
   scopeFrom(principal) ─────▶ TenantScope { tenantId, requestId }
        │
        ▼
   getProjectVisible(scope, id) ─▶ 404 if missing/foreign
        │
        ▼
   archive(scope, project) ──▶ repo.update scoped by tenant_id
        │
        ▼
   audit_log.append(scope, action)
```

Every layer receives the scope; none infers the tenant from the resource id.

## Cache and object keys

```ts
const projectCacheKey = `t:${scope.tenantId}:project:${projectId}`;
const exportObjectKey = `t/${scope.tenantId}/exports/${exportId}.csv`;
```

Reads and writes always prefix the tenant. A helper makes this the only way to build a key:

```ts
function tenantKey(scope: TenantScope, ...parts: string[]) {
  if (!scope.tenantId) throw new MissingTenantScopeError("tenant scope required");
  return `t:${scope.tenantId}:${parts.join(":")}`;
}
```

## Database backstop

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

Even if application code forgets the filter, the policy denies — and because
`current_setting('app.tenant_id')` has no default, an unset scope errors rather than returning rows.

## The isolation test suite

```ts
for (const resource of resources) {
  test(`${resource.name}: foreign == missing (uniform 404)`, async () => {
    const scopeA = { tenantId: "tenant_a", requestId: "r1" };
    const foreign = await createInTenant("tenant_b", resource);
    const resForeign = await request(scopeA, resource, foreign.id);
    const resMissing = await request(scopeA, resource, uuid());
    expect(resForeign.status).toBe(404);
    expect(resForeign.body).toEqual(resMissing.body);   // byte-identical
  });

  test(`${resource.name}: unscoped access fails closed`, async () => {
    await expect(resource.repo({ tenantId: "" } as any).list()).rejects.toThrow(
      "MISSING_TENANT_SCOPE",
    );
  });
}
```

Run the whole matrix per resource type; a new resource without the matrix fails review.

## Key data / numbers

- **OWASP A01/A04**; **CWE-639** (user-controlled key), **CWE-566**.
- **PostgreSQL RLS** with `FORCE` applies to the table owner; unset GUC fails closed.
- **Pooling**: set the tenant GUC transaction-locally (`set_config(..., true)`) so it cannot leak to
  the next request on a reused connection.
- **Key convention**: `t:{tenantId}:` for cache, `t/{tenantId}/` for object stores — one convention.

## Real-world use case — Acme SaaS

Acme added the `ScopedRepo` guard and the per-resource isolation test matrix after a cross-tenant
download incident on `ExportJob` object keys. The matrix immediately failed for two resources
(`documents`, `comments`) that had unscoped `findById` methods — a live bug caught before release.
Fix combined: tenant-prefixed object/cache keys, the scope-required repository, an RLS backstop on the
two tables, and the test matrix as a merge gate. Cross-tenant attempts now return a uniform `404`, and
the fail-closed `MISSING_TENANT_SCOPE` error catches omissions at development time.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Scope-required repo + tests | Catches omissions early | Boilerplate | Every tenant-owned resource |
| App filter only | Simple | One miss = breach | Prototypes only |
| + RLS backstop | Defense in depth | Pooling care | Production multi-tenant |
| Tenant-per-schema | Strongest | Ops overhead | Regulated workloads |

## Common Mistakes

- **Client-supplied tenant on writes.** IDOR via mass assignment.
- **Optional tenant parameter.** The filter you can forget is the filter you will forget.
- **Shared cache/object keys.** Cross-tenant read outside the DB.
- **No isolation test matrix.** The missing test is how the bug ships.
- **Pooled GUC leak.** Scope persists onto the next request.

## Checklist

- [ ] Does every repository require a non-empty `TenantScope`?
- [ ] Are writes' tenant values taken from the scope, not client input?
- [ ] Are cache and object keys always tenant-prefixed?
- [ ] Is there an RLS backstop with a fail-closed GUC?
- [ ] Is the foreign-vs-missing matrix run for every resource?
- [ ] Does unscoped access throw `MISSING_TENANT_SCOPE`?

## Related

- [Tenant Isolation and Context](../01-concepts/04-tenant-isolation-and-context.md)
- [Deep Dive: Tenant Isolation Enforcement](../02-deep-dive/02-tenant-isolation-enforcement.md)
- [Practical: Consistent 401 vs 403](./01-consistent-401-vs-403.md)
- [Chapter 36 — Sensitive Data and Error Context](../../36-sensitive-data-and-error-context/README.md)
- [Glossary](../../../GLOSSARY.md)
