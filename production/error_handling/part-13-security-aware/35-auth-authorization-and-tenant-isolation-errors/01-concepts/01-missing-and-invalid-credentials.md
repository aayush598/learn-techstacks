# Missing and Invalid Credentials

> Part XIII · Chapter 35 · Sections 35.1–35.2 · _Estimated reading time: 15 min_
> **Prerequisite:** [Chapter 34 — Errors as a Disclosure Channel](../../34-security-principles-for-error-handling/01-concepts/01-errors-as-a-disclosure-channel.md)

## In one sentence

**Missing credentials** means the caller presented no identity and warrants a `401` with a
`WWW-Authenticate` challenge; **invalid credentials** means the identity is wrong and must return a
response that does not reveal *which part* was wrong — same status, same code, same message, same
timing.

## Why this matters in production

Authentication is the first trust boundary, and its error responses are the most attacked surface in
any API. Two failure modes dominate:

- **Leaking which credential failed** — "user not found" versus "wrong password" is a free account
  enumeration oracle (see [Chapter 34 §34.9](../../34-security-principles-for-error-handling/01-concepts/04-authorization-disclosure-enumeration-and-timing.md)).
- **Confusing 401 and 403** — clients (and attackers) use the status to infer whether identity or
  permission failed, which leaks whether a token is valid and whether a resource exists.

Getting the status right is also a contract issue: standard clients, OAuth flows, and SDKs react
differently to `401` (refresh token) than to `403` (do not retry).

## Core concept — the two cases

| Case | Meaning | Status | `WWW-Authenticate` | Body |
| ---- | ------- | ------ | ------------------ | ---- |
| **Missing credentials** | No `Authorization` header / no session cookie | `401` | ✅ required | `{ code: "UNAUTHENTICATED" }` |
| **Invalid credentials** | Present but wrong (bad password, bad token) | `401` | ✅ commonly | `{ code: "UNAUTHENTICATED" }` |

The key insight: for all *invalid* credential cases, the response is deliberately **indistinguishable**.
The caller learns only "you are not authenticated" — never which sub-case applied.

## The uniform-401 rule

```text
┌─────────────────────────────────────────────────────────────┐
│ All of these MUST produce the same 401 body + timing:       │
│   • no Authorization header                                  │
│   • malformed Authorization header                           │
│   • unknown user                                             │
│   • wrong password                                           │
│   • unknown token / API key                                  │
│   • expired token                                            │
│   • revoked token                                            │
│   • token for a deleted account                              │
└─────────────────────────────────────────────────────────────┘
```

Sub-cases may differ **internally** (audit, metrics, lockout counters) but never **externally**.

## Worked example — API guard

```ts
// ❌ Distinct codes leak the sub-case.
if (!header) return res.status(401).json({ code: "MISSING_TOKEN" });
if (!valid)  return res.status(401).json({ code: "INVALID_TOKEN" });
if (expired) return res.status(401).json({ code: "TOKEN_EXPIRED" });

// ✅ One external shape; internal reasons for operators only.
const auth = parseAuthorization(req.header("authorization"));

if (!auth) {
  // Missing credentials: send the challenge so clients know how to authenticate.
  res.setHeader("WWW-Authenticate", 'Bearer realm="api", error="invalid_token"');
  return res.status(401).json({ code: "UNAUTHENTICATED", message: "Authentication required." });
}

const principal = await verifyToken(auth.token); // returns null on any failure
if (!principal) {
  // Present but invalid: same status/body shape as missing.
  log.warn({ event: "auth_failed", requestId: req.id, reason: classify(auth) }, "auth failed");
  res.setHeader("WWW-Authenticate", 'Bearer realm="api", error="invalid_token"');
  return res.status(401).json({ code: "UNAUTHENTICATED", message: "Authentication required." });
}
```

The `reason` is logged internally; it never reaches the client.

## Should missing and invalid be byte-identical?

There is a genuine trade-off. A missing header is arguably not secret — the caller knows they sent
none. But `WWW-Authenticate` errors and differing codes can still let an attacker probe token
validity. The safe default is:

- **Same status (`401`) for both.**
- **Same body for both** where practicable; if you differentiate, differentiate only missing (no
  secret implied) and keep all *invalid* cases identical.
- **Always send a challenge** so standards-compliant clients can authenticate.

## Key data / numbers

- **RFC 9110 §15.5.2**: `401 Unauthorized` requires a `WWW-Authenticate` header field carrying at
  least one challenge.
- **RFC 6750** (Bearer tokens): defines `error="invalid_token"`, `error="invalid_request"`,
  `error="insufficient_scope"` in the `WWW-Authenticate` header. `insufficient_scope` is the
  bearer-specific "403-like" case and warrants `403`.
- **OWASP A07: Identification and Authentication Failures**: use generic messages for login errors.
- **CWE-204** (observable response discrepancy): the weakness for differing auth-error codes.

## Real-world use case — Acme SaaS

Acme's API returned three different `401` codes (`MISSING_TOKEN`, `INVALID_TOKEN`, `EXPIRED_TOKEN`).
An attacker used the distinction to probe whether a stolen token was still valid versus whether a
guessed token format was accepted, and to time token-format reconstruction. Fix: all invalid cases
now return a single `UNAUTHENTICATED` code with a Bearer `WWW-Authenticate` challenge; the internal
reason is recorded for operators and drives the "refresh your token" UX client-side via the challenge
rather than a custom code. After the change, probing yielded no signal beyond "not authenticated".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single `UNAUTHENTICATED` for all invalid | No oracle | Less precise client UX | Default |
| Distinct codes for invalid sub-cases | Better DX/debugging | Enumeration of token state | Only if threat model accepts |
| Differentiate only "missing" | Standards-friendly | Slightly more logic | Common compromise |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `401` for all credential failures | Use `403` for a missing token |
| Send a `WWW-Authenticate` challenge | Omit the challenge on `401` |
| Return one code for all invalid cases | Return `NO_USER` / `BAD_PASSWORD` |
| Log the internal reason only | Surface "token expired" to clients |
| Keep timing uniform | Early-return before expensive verification |

## Common mistakes

- **`403` for missing credentials.** The caller is unauthenticated, not forbidden.
- **Distinct expiry code.** It reveals the token was once valid; keep it uniform.
- **No challenge.** Standards clients cannot discover the auth scheme.
- **Leaking via `WWW-Authenticate` error values.** Only use values that do not reveal token state
  (prefer a generic `invalid_token`).

## Checklist

- [ ] Do all invalid-credential cases share one status, code, and message?
- [ ] Is the missing-credential case `401` with a `WWW-Authenticate` challenge?
- [ ] Is the internal reason recorded but never returned?
- [ ] Is timing uniform across missing/invalid/expired?
- [ ] Do Bearer `insufficient_scope` cases use `403`, not `401`?

## Related

- [Session, Token Expiry, and Revocation](./02-session-token-expiry-and-revocation.md)
- [Existence Disclosure and Consistent Status](./05-existence-disclosure-and-consistent-status.md)
- [Practical: Consistent 401 vs 403](../03-practical-examples/01-consistent-401-vs-403.md)
- [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Glossary](../../../GLOSSARY.md)
