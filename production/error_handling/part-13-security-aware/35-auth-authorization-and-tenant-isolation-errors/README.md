# Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors

> Part XIII · _Estimated reading time: 65–85 min_
> **Prerequisite:** [Chapter 34 — Security Principles for Error Handling](../34-security-principles-for-error-handling/README.md)

## One-sentence summary

Authentication and authorization failures are the **most security-sensitive errors a SaaS returns**,
because the *shape* of the error — its status code, message, and timing — can confirm or deny the
existence of accounts, resources, and tenants to callers who must not know.

## Why this chapter matters

Every login, every API call, and every tenant-scoped query passes through an access decision, and
each decision can fail. Handled carelessly, those failures leak: a `403` confirms a workspace exists,
a distinct login code confirms an account is registered, a fast "user not found" confirms the same
with a stopwatch, and a cross-tenant query that "succeeds" with the wrong tenant's data is a breach.
This chapter turns the disclosure principles of Chapter 34 into concrete policy for credentials,
tokens, roles, ownership, tenancy, entitlements, and identity providers.

## Chapter map

The chapter has 15 sections grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-missing-and-invalid-credentials.md`](./01-concepts/01-missing-and-invalid-credentials.md) | 35.1–35.2 | Missing credentials (401 + `WWW-Authenticate`), invalid credentials (uniform 401) |
| [`01-concepts/02-session-token-expiry-and-revocation.md`](./01-concepts/02-session-token-expiry-and-revocation.md) | 35.3–35.4 | Expired sessions/tokens, invalid/revoked tokens, and the uniform response |
| [`01-concepts/03-permissions-and-ownership.md`](./01-concepts/03-permissions-and-ownership.md) | 35.5–35.6 | Insufficient permissions (403), ownership violations (404 vs 403) |
| [`01-concepts/04-tenant-isolation-and-context.md`](./01-concepts/04-tenant-isolation-and-context.md) | 35.7–35.9 | Cross-tenant access, tenant context failures, suspension/entitlement |
| [`01-concepts/05-existence-disclosure-and-consistent-status.md`](./01-concepts/05-existence-disclosure-and-consistent-status.md) | 35.10–35.15 | Avoiding existence disclosure, consistent 401/403, permission-check errors, authz bypass, IdP failures, secure failure for auth deps |
| [`02-deep-dive/01-consistent-401-vs-403.md`](./02-deep-dive/01-consistent-401-vs-403.md) | 35.10–35.12 (mechanics) | The decision tree, middleware mechanics, and fail-closed behavior |
| [`02-deep-dive/02-tenant-isolation-enforcement.md`](./02-deep-dive/02-tenant-isolation-enforcement.md) | 35.7–35.8 (mechanics) | Where tenant context is set, propagated, and enforced; row-level security |
| [`02-deep-dive/03-identity-provider-and-policy-engine-failures.md`](./02-deep-dive/03-identity-provider-and-policy-engine-failures.md) | 35.13–35.15 (mechanics) | IdP/broker outages, policy-engine errors, and secure failure modes |
| [`03-practical-examples/01-consistent-401-vs-403.md`](./03-practical-examples/01-consistent-401-vs-403.md) | 35.1–35.5, 35.11 | A middleware stack returning consistent, non-revealing auth/authz errors |
| [`03-practical-examples/02-tenant-isolation-check.md`](./03-practical-examples/02-tenant-isolation-check.md) | 35.6–35.8, 35.10 | A tenant-scoping guard that makes cross-tenant access return the uniform 404 |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Auth/authz/tenancy rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Status decision tree, header rules, tenant-isolation checklist |

## Learning objectives

By the end you can:

- Return **`401` for missing/invalid credentials** with the correct `WWW-Authenticate` behavior, and
  **`403` only when existence is safe to reveal**.
- Make session expiry, revocation, and invalid tokens **indistinguishable** to callers.
- Apply **ownership and permission checks** that never confirm a resource the caller cannot see.
- Enforce **tenant isolation** so cross-tenant access returns the uniform, non-revealing outcome.
- Handle **IdP and policy-engine failures fail-closed** and never convert them to a bypass.
- Keep the auth/authz error **contract consistent** across endpoints, services, and the frontend.

## Key takeaways

1. **401 means "I don't know who you are"; 403 means "I know you and you may not".** Confusing them
   leaks identity state.
2. **404 is often the most secure authorization answer** when the caller must not learn that a
   resource exists.
3. **The whole auth pipeline matters, not just login.** Expiry, revocation, ownership, tenant scope,
   and entitlement all produce errors a caller can read.
4. **Cross-tenant access must be a non-event in the response**: identical to a real not-found.
5. **Authorization dependencies fail closed.** An unavailable policy engine denies; it never allows.
6. **Consistency is a security property.** If one endpoint leaks via a distinct code, attackers only
   need to find that endpoint.

## Exercises

1. List every endpoint that returns `401`/`403`/`404` and record the exact body for each. Flag any
   pair that differs for cases a caller must not distinguish.
2. Take a resource endpoint and confirm that requesting another tenant's id returns a body
   **byte-identical** to requesting a nonexistent id.
3. Inject an exception into your policy-engine call and verify the request is denied and alarmed.
4. Write the `WWW-Authenticate` behavior for your API: when is it sent, and does the challenge
   itself leak anything?
5. Map entitlement/suspension errors: does the response reveal that an account exists but is
   suspended? Decide whether that is acceptable for your threat model and document it.

## Related

- [Chapter 34 — Security Principles for Error Handling](../34-security-principles-for-error-handling/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../36-sensitive-data-and-error-context/README.md)
- [Chapter 19 — HTTP Error Semantics](../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Glossary](../../GLOSSARY.md)
