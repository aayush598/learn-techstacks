# Authorization Disclosure, Enumeration, and Timing

> Part XIII · Chapter 34 · Sections 34.8–34.10 · _Estimated reading time: 17 min_
> **Prerequisite:** [Secrets, PII, and Tenant Leakage](./03-secrets-pii-and-tenant-leakage.md)

## In one sentence

An error that *distinguishes* cases an attacker should not be able to tell apart — **which
resource exists**, **which account is registered**, or **which comparison ran** — turns your error
handling into an oracle; the fix is uniform responses and constant-work paths.

## Why this matters in production

Three related disclosure bugs, each cheap to fix and expensive to ignore:

- **Authorization disclosure** — returning `403 Forbidden` for a resource the caller may not know
  exists confirms its existence. `404` reveals nothing.
- **User enumeration** — different responses (or status codes) for "unknown user" versus "wrong
  password" let an attacker harvest a list of valid accounts, which they then phish or credential-stuff.
- **Timing disclosure** — if "unknown user" returns in 3 ms and "wrong password" in 90 ms (because
  only the second runs the password hash), an attacker with a stopwatch enumerates without a single
  differing character.

These are not exotic. They appear in default framework behavior, in `if (!user) return 401` code,
and in any comparison written with `===` instead of a constant-time primitive.

## The three oracles

| Oracle | Signal an error must not correlate with | Common cause |
| ------ | --------------------------------------- | ------------ |
| **Existence / authorization** | Whether a resource or account exists | `403` vs `404`; distinct messages like "no such workspace" |
| **Enumeration** | Whether an identifier is valid/registered | Different codes for "unknown email" vs "bad password"; signup "email taken" without rate limits |
| **Timing** | How much work was done | Early return before hashing; non-constant-time string/byte comparison |

## How it works (mechanics)

### Uniform responses

The rule is simple: **cases an attacker must not distinguish get the same status, the same body
shape, and the same timing profile.**

| Scenario | Naive response | Safe response | Why |
| -------- | -------------- | ------------- | --- |
| Login, unknown user | `401 {code:"NO_USER"}` | `401 {code:"INVALID_CREDENTIALS"}` | Same as wrong password |
| Login, wrong password | `401 {code:"BAD_PASSWORD"}` | `401 {code:"INVALID_CREDENTIALS"}` | — |
| Reset password, unknown email | `404 {code:"NO_USER"}` | `200 {message:"If an account exists, we sent a link"}` | Do not confirm registration |
| Signup, email taken | `409 {code:"EMAIL_TAKEN"}` | `200` generic or rate-limited flow | Avoids account harvesting at scale |
| Resource in another tenant | `403 {code:"FORBIDDEN"}` | `404 {code:"NOT_FOUND"}` | Do not confirm existence |

### Constant-time comparison

String comparison in most languages short-circuits at the first mismatched byte. That means the
time to compare a guess against a secret correlates with **how many leading bytes are correct** —
enough information, in principle, to reconstruct the secret byte by byte. This applies to:

- Password verification (compare **derived hashes**, not raw, and compare them constantly).
- HMAC/signature verification (Stripe webhook signatures, JWT signatures).
- API key and bearer token lookups.

Use the platform's constant-time primitive:

```ts
import { timingSafeEqual } from "node:crypto";

function safeEqual(a: Buffer, b: Buffer): boolean {
  // timingSafeEqual requires equal lengths; pad/hash to fixed length instead of early-returning.
  if (a.length !== b.length) {
    // Compare against a fixed dummy to keep timing stable, then return false.
    timingSafeEqual(a, Buffer.alloc(a.length));
    return false;
  }
  return timingSafeEqual(a, b);
}
```

```python
import hmac
# Constant-time comparison of two digests (equal length).
def safe_equal(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
```

```go
import "crypto/subtle"
// Constant-time equality for equal-length byte slices.
ok := subtle.ConstantTimeCompare(a, b) == 1
```

### Constant-work authentication paths

Uniform messages are not enough if the timing differs. The standard pattern is **always do the same
work**:

1. Look up the user.
2. If no user, substitute a **dummy user record** with a valid password hash.
3. Always run the password hash comparison.
4. Return the same generic failure.

This makes "unknown user" and "wrong password" take similar time, so the login endpoint is not a
timing oracle. The dummy hash must be a real, current-algorithm hash so the work is comparable.

```ts
async function authenticate(email: string, password: string): Promise<Session | null> {
  const user = await users.findByEmail(email);

  // Always compare against *something* hashed with the same algorithm/cost.
  const hash = user?.passwordHash ?? DUMMY_HASH; // DUMMY_HASH is a real argon2/bcrypt hash
  const ok = await verifyPassword(password, hash);

  if (!user || !ok) {
    return null; // caller maps to a single generic 401
  }
  return createSession(user);
}
```

## Key data / numbers

- **OWASP Top 10 (2021) A07: Identification and Authentication Failures** explicitly names user
  enumeration and describes uniform error messages as a mitigation.
- **CWE-259** (hard-coded password), **CWE-203: Observable Discrepancy** (timing side channels),
  **CWE-204: Observable Response Discrepancy** (differing responses that leak state).
- **HTTP choice**: for authenticated-resource ownership, prefer **`404 Not Found`** over **`403
  Forbidden`** when existence itself is sensitive. Use `403` only when the caller legitimately knows
  the resource exists and is denied by role.
- **Rate limiting** is a partial mitigation for enumeration but not a fix; pair uniform responses
  with per-IP and per-account rate limits (see [Chapter 21](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)).
- **Timing tolerance**: aim for the login path's unknown-user vs wrong-password latency difference
  to be within noise (commonly single-digit milliseconds, well under typical network jitter). Measure
  with enough samples to separate signal from jitter.

## Real-world use case — Acme SaaS

Acme's login returned `{"code":"USER_NOT_FOUND"}` for unknown emails and `{"code":"WRONG_PASSWORD"}`
for known ones, and skipped hashing when the user was missing. A red team harvested 40,000 valid
tenant emails in under an hour using the distinct codes and confirmed the timing gap with a script.
Fix: (1) both cases now return the identical `401 {"code":"INVALID_CREDENTIALS"}`; (2) the codebase
always runs `verifyPassword` against `DUMMY_HASH` when the user is missing; (3) the password-reset
endpoint now returns a uniform `200` "if an account exists…". Post-fix measurement showed the two
paths within measurement noise, and enumeration required guessing, not reading.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Uniform generic code | No oracle | Slightly worse UX ("what went wrong?") | All credential checks |
| Distinct codes + strict rate limit | Better UX | Still enumerable over time | Only when existence is not sensitive |
| Dummy-hash constant-work auth | No timing oracle | Small extra CPU per miss | All login/reset paths |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return one generic code for all login failures | Say "no such user" |
| Run a dummy hash when the user is missing | Early-return before hashing |
| Use `timingSafeEqual`/`compare_digest`/`subtle` | Compare secrets with `==` |
| Return `404` for opaque/other-tenant resources | Return `403` that confirms existence |
| Make reset/signup responses uniform | Confirm registration status |

## Common mistakes

- **Uniform message, non-uniform time.** The body matches but the latency leaks.
- **Comparing raw secrets.** Compare derived hashes/signatures, and compare them constantly.
- **Padded-but-short-circuiting comparison.** A manual "constant-time" function that still
  early-returns on length is not constant-time.
- **Assuming rate limiting closes enumeration.** It slows it; it does not remove the oracle.
- **Leaking via response size.** Different message lengths can be distinguished even with the same
  status code; keep bodies identical.

## Checklist

- [ ] Do all login failure cases return an identical status, code, message, and body length?
- [ ] Does the code run a dummy password hash when the user is not found?
- [ ] Are all secret/signature comparisons constant-time?
- [ ] Do password-reset and signup avoid confirming account existence?
- [ ] Do other-tenant resources return `404` rather than a distinguishing `403`?
- [ ] Have you measured the timing of the auth path, not just the response body?

## Related

- [Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors](../../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Deep dive: Timing Attacks and User Enumeration](../02-deep-dive/02-timing-attacks-and-user-enumeration.md)
- [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
