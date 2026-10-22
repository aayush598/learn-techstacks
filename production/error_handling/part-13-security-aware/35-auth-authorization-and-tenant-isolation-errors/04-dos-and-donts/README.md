# Chapter 35 — Do's and Don'ts

> Part XIII · Chapter 35 · all sections · _Estimated reading time: 9 min_

## In one sentence

Authentication, authorization, and tenant errors are safe when the **access path is centralized,
ordered (authenticated → visible → permitted), consistent (four outcomes), and fail-closed**, and when
no response distinguishes cases a caller must not tell apart.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | Return `401` for all credential failures | Return `403` for missing credentials |
| 2 | Send `WWW-Authenticate` on `401` | Omit the challenge |
| 3 | One code for invalid/expired/revoked tokens | Expose token lifecycle state |
| 4 | Deny (`403`/`404`) on policy-engine error | Fail open |
| 5 | Fail **closed** on IdP/session-store outage | Accept unverifiable tokens |
| 6 | Verify signatures (`verify`, not `decode`) | `jwt.decode()` on fetch failure |
| 7 | Resolve existence before permissions | Check role first |
| 8 | Return uniform `404` for hidden/foreign | Return a distinguishing `403` |
| 9 | Keep foreign/missing body + timing identical | Different messages for the two |
| 10 | Use `403 insufficient_scope` for Bearer scope | Return `401` for a scope failure |
| 11 | Derive tenant from the authenticated principal | Trust `X-Tenant-Id` alone |
| 12 | Fail closed on missing tenant scope | Treat no tenant as all tenants |
| 13 | Scope every query, cache key, object key, job | Assume the handler scoped it |
| 14 | Add an RLS/policy backstop | Rely only on app filters |
| 15 | Set tenant GUC transaction-local on pools | Let the GUC persist across requests |
| 16 | Ignore client-supplied tenant on writes | Trust a client `tenantId` field |
| 17 | Alarm on `authz_check_error_total` | Swallow policy-engine errors |
| 18 | Cache decisions only for low-risk reads | Cache write/admin decisions |
| 19 | Bound JWKS freshness and staleness | Trust keys indefinitely |
| 20 | Run a foreign-vs-missing test per resource | Ship endpoints without it |

## Anti-patterns with symptoms

### ❌ `403` for cross-tenant resources

```ts
if (project.tenantId !== principal.tenantId) throw new ForbiddenError();
```

**Symptom:** attackers enumerate real workspace/project ids by the `403` vs `404` difference.
**Fix:** merge hidden and missing into one uniform `404`.

### ❌ Fail-open authorization

```ts
function can(...) { try { return engine.check(...); } catch { return true; } }
```

**Symptom:** a policy-engine or IdP outage becomes a full authorization bypass.
**Fix:** deny on error; alarm on `authz_check_error_total`.

### ❌ `decode` instead of `verify`

```ts
const claims = jwt.decode(token); // no signature check
```

**Symptom:** forged tokens accepted, including other tenants' identities.
**Fix:** verify signatures; reject when the key cannot be fetched.

### ❌ Trusting the tenant header

```ts
const tenantId = req.header("x-tenant-id"); // client-controlled
```

**Symptom:** set `X-Tenant-Id: victim` and read victim data (IDOR).
**Fix:** tenant comes from the authenticated principal.

### ❌ Unscoped cache key

```ts
const key = `project:${id}`; // no tenant
```

**Symptom:** one tenant reads another's cached data.
**Fix:** `t:{tenantId}:project:{id}`.

### ❌ Missing scope widening access

```ts
const rows = await db.query("SELECT * FROM items"); // no tenant filter
```

**Symptom:** cross-tenant read; the worst default.
**Fix:** require a `TenantScope`; throw `MISSING_TENANT_SCOPE` when absent.

### ❌ Distinct token lifecycle codes

```ts
return res.status(401).json({ code: "TOKEN_REVOKED" });
```

**Symptom:** attackers confirm which stolen tokens were detected and killed.
**Fix:** one `UNAUTHENTICATED`.

### ❌ Handler overriding access status

```ts
if (bad) return res.status(403).json(...); // inside a handler
```

**Symptom:** inconsistent statuses across endpoints; an enumeration oracle.
**Fix:** centralize the 401/403/404 decision in middleware.

## Code-review questions

1. Which of the four outcomes does this access path return, and is it consistent with other endpoints?
2. Is the order authenticated → visible → permitted?
3. Could a hidden resource be distinguished from a missing one (status, body, timing)?
4. Does any authz/IdP error allow instead of deny?
5. Is the tenant derived from the principal, never a header/id?
6. Are all queries, cache keys, object keys, and jobs tenant-scoped?
7. Is there an RLS/backstop policy?
8. Is there a foreign-vs-missing test for this resource?

## Minimal policy snippet

```yaml
accessPolicy:
  order: [authenticated, visible, permitted]
  outcomes:
    unauthenticated: { status: 401, code: UNAUTHENTICATED, challenge: invalid_token }
    hiddenOrMissing: { status: 404, code: NOT_FOUND, uniform: true }
    denied:          { status: 403, code: FORBIDDEN }
    scopeMissing:    { status: 403, code: INSUFFICIENT_SCOPE, challenge: insufficient_scope }
  failClosed: [policyError, idpError, missingTenantScope]
  tenantFrom: principal
  scopeRequired: true
  rlsBackstop: true
  alarm: authz_check_error_total
```

## Related

- [Existence Disclosure and Consistent Status](./../01-concepts/05-existence-disclosure-and-consistent-status.md)
- [Tenant Isolation and Context](./../01-concepts/04-tenant-isolation-and-context.md)
- [Chapter 35 Reference](../05-reference/README.md)
- [Chapter 34 — Security Principles Do's and Don'ts](../../34-security-principles-for-error-handling/04-dos-and-donts/README.md)

