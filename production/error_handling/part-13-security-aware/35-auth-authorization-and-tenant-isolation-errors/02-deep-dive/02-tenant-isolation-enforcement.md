# Deep Dive — Tenant Isolation Enforcement

> Part XIII · Chapter 35 · Sections 35.7–35.8 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Tenant Isolation and Context](../01-concepts/04-tenant-isolation-and-context.md)

## In one sentence

Tenant isolation is enforced by **carrying an explicit tenant scope on every unit of work and
verifying it at the data layer** (query filter + row-level security + scoped cache/object keys), so
that a cross-tenant attempt produces the uniform `404` and an unscoped access **fails closed** instead
of widening.

## Why this matters in production

The most damaging SaaS bugs are not permission mistakes at one endpoint — they are **missing
scopes**. A repository method without a tenant filter, a cache key without a tenant prefix, an S3 key
without a tenant path, or a background job that runs "for the system" without a tenant: each is a
cross-tenant read or write waiting to happen. Defense in depth means the *last* layer (the database)
denies by default even when the application forgets — this file is how to build that.

## The scope object

Carry tenant scope explicitly, never implicitly:

```ts
interface TenantScope {
  readonly tenantId: string;   // required, non-empty
  readonly userId?: string;    // for audit
  readonly requestId: string;  // for correlation
}

// Constructed once, at the edge, from the authenticated principal.
function scopeFrom(principal: Principal, req: Request): TenantScope {
  if (!principal.tenantId) throw new InternalError("MISSING_TENANT_SCOPE"); // fail closed
  return { tenantId: principal.tenantId, userId: principal.id, requestId: req.id };
}
```

Pass `TenantScope` into every repository call. A missing scope is a programming error that throws
internally — it never defaults to "all tenants".

## Layer 1 — Application scoping

```ts
class ProjectRepository {
  constructor(private db: Db, private scope: TenantScope) {}

  async findById(id: string): Promise<Project | null> {
    // The tenant filter is not optional; it comes from the scope.
    return this.db.one<Project>(
      "SELECT * FROM projects WHERE id = $1 AND tenant_id = $2",
      [id, this.scope.tenantId],
    );
  }

  async list(): Promise<Project[]> {
    return this.db.many<Project>(
      "SELECT * FROM projects WHERE tenant_id = $1 ORDER BY created_at DESC",
      [this.scope.tenantId],
    );
  }
}
```

Every read and write includes `tenant_id = $2`. There is no `findByIdUnscoped`.

## Layer 2 — Database backstop (PostgreSQL RLS)

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;

-- Fail-closed: current_setting with no default raises if unset.
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

```ts
// Set the tenant GUC per transaction/connection before queries.
async function withTenant<T>(pool: Pool, tenantId: string, fn: (c: Client) => Promise<T>) {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    await client.query("SELECT set_config('app.tenant_id', $1, true)", [tenantId]);
    const result = await fn(client);
    await client.query("COMMIT");
    return result;
  } catch (e) {
    await client.query("ROLLBACK");
    throw e;
  } finally {
    client.release();
  }
}
```

Because the policy uses `current_setting('app.tenant_id')` **without a default**, an unset scope makes
the query error rather than return rows — fail closed at the database.

> ⚠️ **Hazard.** If you use a **connection pool**, the tenant GUC must be set transaction-locally
> (`set_config(..., true)`) or reset on release. A leaked GUC on a pooled connection scopes the *next*
> tenant's query to the *previous* tenant — a cross-tenant read.

## Layer 3 — Caches, object stores, queues

| Resource | Rule |
| -------- | ---- |
| Redis/cache key | `t:{tenantId}:{...}` — never a bare key |
| S3/object key | `t/{tenantId}/...` — tenant path prefix |
| Queue message | carries `tenantId`; consumer re-derives scope from it |
| Rate limiter | keyed per tenant (and per user) |
| Search index | documents filtered by `tenant_id` |

```ts
const cacheKey = `t:${scope.tenantId}:project:${id}`;
const objectKey = `t/${scope.tenantId}/exports/${exportId}.csv`;
```

A shared key across tenants is a cross-tenant read; a shared object key is a cross-tenant download.

## Background work

Jobs and consumers run without a request, so they must reconstruct scope from the message:

```python
def handle_export(message):
    scope = TenantScope(tenant_id=message["tenantId"], request_id=message["requestId"])
    if not scope.tenant_id:
        raise NonRetryableError("MISSING_TENANT_SCOPE")  # fail closed, route to DLQ
    with with_tenant(scope.tenant_id):
        run_export(scope, message)
```

Never run a job "for all tenants" without an explicit, audited system scope.

## Verification in CI

```ts
test("cross-tenant access is a uniform 404", async () => {
  const a = await tokenFor("tenant_a");
  const projB = await createProject("tenant_b");
  const res = await get(`/projects/${projB.id}`, a);
  const missing = await get(`/projects/${uuid()}`, a);
  expect(res.status).toBe(404);
  expect(res.body).toEqual(missing.body);
});
```

Run this for every resource type; a new endpoint without this test is a review block.

## Key data / numbers

- **OWASP A01**, **A04**, **CWE-639**, **CWE-566**: cross-tenant access via missing scoping.
- **PostgreSQL RLS**: `FORCE ROW LEVEL SECURITY` applies policy even to the table owner;
  `current_setting('app.tenant_id')` without a default fails closed.
- **Pooling caveat**: set the GUC `is_local = true` (transaction-scoped) or reset on return, or the
  scope leaks across pooled requests.
- **Cache/object prefix convention**: `t:{tenantId}:` / `t/{tenantId}/` — one convention everywhere.

## Real-world use case — Acme SaaS

Acme's search feature cached results in Redis under `search:{queryHash}` — no tenant prefix. Tenant B's
search for "quarterly report" returned tenant A's cached document titles. Fix: keys became
`t:{tenantId}:search:{queryHash}`, results were filtered by `tenant_id` in the query, an RLS policy was
added as a backstop, and a CI test asserted no cross-tenant result appears for a set of crafted queries.
The incident was found by a tenant; the fix added the missing tenant dimension to all three layers.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| App-layer scoping only | Portable, simple | One miss = breach | Prototypes, with strong tests |
| App + RLS | Defense in depth | DB-specific; pooling care | Multi-tenant production |
| Tenant-per-schema/DB | Strongest isolation | Ops overhead, migrations ×N | Regulated/high-assurance |

## Common mistakes

- **Optional tenant filter.** A filter you can forget is a filter you will forget.
- **Pooled connection with a leaked GUC.** Cross-tenant on the next request.
- **Cache/object keys without tenant.** Data leaks outside the DB.
- **Background jobs without tenant scope.** Unscoped reads.
- **No CI cross-tenant test.** The missing test is how the bug ships.

## Checklist

- [ ] Does every repository call take an explicit `TenantScope`?
- [ ] Does a missing scope throw internally (fail closed)?
- [ ] Is there an RLS/policy backstop at the database?
- [ ] Are cache keys, object keys, and queue messages tenant-scoped?
- [ ] Are the tenant GUC and scope transaction-local on pooled connections?
- [ ] Is cross-tenant access byte-identical to not-found in a CI test per resource?

## Related

- [Tenant Isolation and Context](../01-concepts/04-tenant-isolation-and-context.md)
- [Consistent 401 vs 403](./01-consistent-401-vs-403.md)
- [Practical: Tenant Isolation Check](../03-practical-examples/02-tenant-isolation-check.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
- [Glossary](../../../GLOSSARY.md)
