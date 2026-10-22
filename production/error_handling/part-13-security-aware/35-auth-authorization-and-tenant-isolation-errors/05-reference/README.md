# Chapter 35 — Reference

> Part XIII · Chapter 35 · all sections · _Estimated reading time: 13 min_

## The four access outcomes

| Condition | Status | Code | Header | Rationale |
| --------- | ------ | ---- | ------ | --------- |
| Not authenticated (missing/invalid/expired/revoked) | `401` | `UNAUTHENTICATED` | `WWW-Authenticate: invalid_token` | Identity unknown |
| Resource hidden or missing | `404` | `NOT_FOUND` | — | Do not confirm existence |
| Authenticated, visible, role denied | `403` | `FORBIDDEN` | — | Existence known, action denied |
| Authenticated, Bearer scope missing | `403` | `INSUFFICIENT_SCOPE` | `WWW-Authenticate: insufficient_scope` | RFC 6750 |

## Status decision tree

```text
authenticated?
  no ─────────────────────────────▶ 401 (+WWW-Authenticate)
  yes
    resource visible to this caller?
      no (missing OR foreign) ─────▶ 404 (uniform, identical body/timing)
      yes
        permitted (role/scope)?
          no, scope ───────────────▶ 403 insufficient_scope
          no, role ────────────────▶ 403 FORBIDDEN
          yes ─────────────────────▶ handler
```

Order is fixed: **authenticated → visible → permitted.**

## Which cases must be identical

| Group | Must share status + body + timing | Leaks otherwise |
| ----- | --------------------------------- | --------------- |
| Unknown user / wrong password | ✅ | Account existence |
| Expired / revoked / invalid / deleted-account token | ✅ | Token lifecycle & incident state |
| Missing / other-tenant resource | ✅ | Resource existence |
| Invalid / used invite code | ✅ | Code validity |

## Auth dependency failure behavior

| Failure | Behavior | Never |
| ------- | -------- | ----- |
| JWKS unreachable | Reject / `503`; bounded-stale cache | `decode` without verify |
| Unknown `kid` | Refresh once, then reject | Accept unverified |
| Session store down | `503` | Fabricate session |
| Policy engine error/timeout | Deny + alarm | Allow |
| Config missing at boot | Fail startup | Serve with checks off |
| Clock skew | Small skew (≈60 s); monitor | Disable expiry |

## Tenant isolation checklist

| Layer | Requirement |
| ----- | ----------- |
| Context | Tenant from authenticated principal, never a header alone |
| Repository | `TenantScope` required; missing scope throws |
| Queries | `WHERE tenant_id = :tid` on every read/write |
| Writes | Tenant value from scope, not client input |
| Cache keys | `t:{tenantId}:...` |
| Object keys | `t/{tenantId}/...` |
| Queue/jobs | Carry `tenantId`; consumer re-scopes |
| Database | RLS/policy backstop, fail-closed GUC |
| Pools | Tenant GUC transaction-local |
| Tests | foreign-vs-missing byte-identical per resource |

## Headers quick reference

| Header | When | Example |
| ------ | ---- | ------- |
| `WWW-Authenticate` (401) | Missing/invalid credentials | `Bearer realm="api", error="invalid_token"` |
| `WWW-Authenticate` (403) | Bearer scope missing | `Bearer realm="api", error="insufficient_scope", scope="exports:read"` |
| `Retry-After` (503) | Auth dependency outage | `30` |

## Standards & weaknesses

| Topic | Reference |
| ----- | --------- |
| 401 requires challenge | RFC 9110 §15.5.2 |
| 403 meaning | RFC 9110 §15.5.4 |
| Bearer errors | RFC 6750 (`invalid_token`, `insufficient_scope`) |
| Broken access control | OWASP A01, A04 |
| Auth failures | OWASP A07 |
| Observable discrepancy | CWE-204, CWE-203, CWE-208 |
| Authz bypass / IDOR | CWE-639, CWE-566, CWE-863, CWE-285 |
| Signature verification | CWE-347 |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Principal** | The authenticated identity (user + tenant + role + scopes) |
| **Tenant scope** | The explicit tenant context carried with every unit of work |
| **Existence disclosure** | Revealing whether a resource/account exists |
| **Uniform 404** | Identical response for hidden and missing resources |
| **Fail closed** | Deny on error; the security default |
| **Fail open** | Allow on error; a bypass anti-pattern |
| **RLS** | Row-Level Security; database-enforced tenant filtering |
| **GUC** | PostgreSQL session/transaction setting (e.g. `app.tenant_id`) |
| **Insufficient scope** | RFC 6750 Bearer-token authorization failure (`403`) |
| **IDOR** | Insecure Direct Object Reference; access via client-controlled key |

## Related

- [Chapter 35 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Deep Dive: Consistent 401 vs 403](../02-deep-dive/01-consistent-401-vs-403.md)
- [Deep Dive: Tenant Isolation Enforcement](../02-deep-dive/02-tenant-isolation-enforcement.md)
- [Chapter 34 — Security Principles for Error Handling](../../34-security-principles-for-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)

