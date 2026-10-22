# Existence Disclosure and Consistent Status

> Part XIII · Chapter 35 · Sections 35.10–35.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Tenant Isolation and Context](./04-tenant-isolation-and-context.md)

## In one sentence

**Avoiding existence disclosure** means opaque resources share one outcome; **consistent 401/403**
means every endpoint answers the same access question the same way; and **errors during permission
checks, authorization bypass, and IdP failures** must all **fail closed** — never converting an
unavailable dependency into an access grant.

## Why this matters in production

Inconsistency is itself a vulnerability: an attacker probes every endpoint, and the *one* that
returns a distinct code reveals the resource/inventory. Likewise, an authorization path that
"continues on error" turns a transient outage into a breach. This section is the integration point:
it binds the earlier concepts (401/403, existence, tenancy) into one coherent, fail-closed,
non-revealing contract that every endpoint shares.

## Avoiding existence disclosure

| Resource kind | Existence private? | Denied access response |
| ------------- | ------------------ | ---------------------- |
| Private workspace/project/doc | ✅ | `404` (uniform) |
| Public profile | ❌ | `403` acceptable |
| API key / token id | ✅ | `404` / `401` uniform |
| Email/account at login/reset | ✅ | uniform success/`401` |
| Invite code | ✅ | `404` (uniform with invalid) |

The rule: **if revealing existence could help an attacker, the denied and the absent responses are
identical** — status, body, and timing.

## Consistent 401 vs 403 across endpoints

```text
Every endpoint answers these the same way:

 not authenticated ......................... 401 UNAUTHENTICATED
 authenticated, resource hidden from them ... 404 NOT_FOUND
 authenticated, resource visible, role low .. 403 FORBIDDEN
 authenticated, scope missing (Bearer) ...... 403 insufficient_scope
```

> ⚠️ **Hazard.** A single endpoint that returns `403` where others return `404` hands the attacker
> the enumeration signal the whole design tried to remove. Consistency is enforced by shared
> middleware, not by each handler.

## Errors during permission checks

A permission check can itself fail — the policy engine times out, the ACL lookup errors, a rule
throws. The only safe handling is **deny**:

```ts
// ❌ Fail-open: any check error becomes an authorization bypass.
function can(principal, action, resource) {
  try { return policyEngine.check(principal, action, resource); }
  catch { return true; } // ✗ catastrophic
}

// ✅ Fail-closed: a check error denies and alarms.
function can(principal, action, resource): boolean {
  try {
    return policyEngine.check(principal, action, resource);
  } catch (e) {
    metrics.increment("authz_check_error_total"); // page on this
    log.error({ event: "authz_check_failed", requestId }, "policy engine error");
    return false; // deny
  }
}
```

A check that cannot complete is **not** a "maybe"; it is a "no".

## Authorization errors bypassing business rules

Authorization must not be skippable by business-logic shortcuts. Two anti-patterns:

- **Early return before authz**: an "if cached, return early" path that skips the permission check.
- **Authz only in the handler, not in the domain/service**: a service method callable from multiple
  entry points that each remember (or forget) to authorize.

Authz belongs on every path that reaches data, including caches and background jobs. The error
contract must make a bypass *impossible*, not merely unlikely: centralize the check in the data
access layer (see [tenant isolation enforcement](../02-deep-dive/02-tenant-isolation-enforcement.md)).

## Identity provider and policy-engine failures

| Dependency | Failure | Correct behavior |
| ---------- | ------- | ---------------- |
| IdP (OIDC) unreachable | Cannot verify token | Fail closed: `503`, not accept |
| JWKS fetch fails | Cannot validate signature | Fail closed; use a safely cached JWKS with bounded staleness |
| Policy engine down | Cannot decide | Deny (`403`/`404`), alarm; never allow |
| Introspection endpoint down | Cannot confirm token | Fail closed (`503`) |
| Session store down | Cannot read session | `503`; do not fabricate a session |

Never **cache a positive authorization decision** across a context change, and never lengthen a
token's validity to "ride out" an IdP outage. Availability pressure is exactly when fail-open bugs
get introduced.

## Worked example — uniform access contract

```ts
function accessError(err: unknown): AuthError {
  if (err instanceof NotFoundError) return new AuthError("NOT_FOUND", 404);
  if (err instanceof ForbiddenError) return new AuthError("FORBIDDEN", 403);
  if (isPolicyEngineDown(err)) {
    metrics.increment("authz_check_error_total");
    return new AuthError("FORBIDDEN", 403); // deny on dependency failure
  }
  return new AuthError("INTERNAL_ERROR", 500); // unknown → safe default
}

// Every handler funnels through this; no handler crafts its own status.
```

## Key data / numbers

- **OWASP A01: Broken Access Control** — fail-open authorization and inconsistent responses are its
  documented vectors.
- **CWE-863: Incorrect Authorization**, **CWE-285: Improper Authorization**, **CWE-639** (IDOR).
- **RFC 6750**: `insufficient_scope` → `403`; a missing/invalid token → `401`.
- **JWKS caching**: cache keys with a bounded TTL and a negative-cache guard; on fetch failure, reject
  rather than accept with unverifiable signatures.
- **Alarm threshold**: any non-zero `authz_check_error_total` should page — it means a decision could
  not be made.

## Real-world use case — Acme SaaS

Acme's `AgentRun` feature fetched an external "policy" JSON to decide whether a tool call was
allowed, and cached the result for one hour. During an IdP incident, the cache was cold and the fetch
failed; the code fell back to `return true` "to avoid breaking agents". Every tool became allowed for
every tenant for the duration of the outage. Fix: the fallback now denies, a bounded-staleness JWKS
and policy cache is used (accept cached decisions only briefly and only for low-risk actions), and
`authz_check_error_total` pages immediately. A test injects a policy-fetch failure and asserts the
tool call is denied.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fail closed everywhere | No bypass | Availability dips when authz deps fail | All access decisions |
| Bounded-staleness cache for low-risk | Preserves some availability | Must bound time & risk | Read-only low-risk checks |
| Fail open | Availability | Authorization bypass | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize the 401/403/404 decision | Let handlers craft their own |
| Deny when an authz check errors | `catch { return true; }` |
| Alarm on authz-check errors | Silently swallow them |
| Use bounded-staleness caches only for low risk | Trust a stale positive decision |
| Keep hidden and absent responses identical | Differentiate them anywhere |

## Common mistakes

- **One endpoint returning `403` where others return `404`.** The enumeration signal.
- **Fail-open policy checks.** The catastrophic one.
- **Authz only at the handler.** Bypassed via caches/background paths.
- **Accepting unverifiable tokens during a JWKS outage.** Fail closed.
- **Caching a positive decision across a context change.** Stale grants.

## Checklist

- [ ] Do all endpoints share one 401/403/404 decision function?
- [ ] Are hidden and absent resources indistinguishable everywhere?
- [ ] Do authz and IdP failures deny (or `503`), never allow?
- [ ] Is `authz_check_error_total` alarmed?
- [ ] Is authz enforced on cache-hit and background paths too?
- [ ] Are JWKS/policy caches bounded in staleness and scope?

## Related

- [Permissions and Ownership](./03-permissions-and-ownership.md)
- [Tenant Isolation and Context](./04-tenant-isolation-and-context.md)
- [Deep dive: Consistent 401 vs 403](../02-deep-dive/01-consistent-401-vs-403.md)
- [Deep dive: Identity Provider and Policy Engine Failures](../02-deep-dive/03-identity-provider-and-policy-engine-failures.md)
- [Glossary](../../../GLOSSARY.md)
