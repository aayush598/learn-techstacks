# Session, Token Expiry, and Revocation

> Part XIII · Chapter 35 · Sections 35.3–35.4 · _Estimated reading time: 15 min_
> **Prerequisite:** [Missing and Invalid Credentials](./01-missing-and-invalid-credentials.md)

## In one sentence

**Expired** sessions/tokens and **invalid or revoked** tokens are different internal events but must
produce the **same external `401`** — the caller learns only "authenticate again", never whether the
token was once valid, deliberately revoked, or never existed.

## Why this matters in production

Token state is security-sensitive information:

- **"Expired" vs "revoked"** tells an attacker whether a stolen token is still within its validity
  window (worth trying to use quickly) or has been killed (compromised). Distinguishing them is a
  hint about your incident response.
- **"Revoked" can reveal that a session was terminated** — for example, that a user reported a
  compromise, which is itself sensitive.
- **Distinct codes create a state machine the client can probe**: valid → expired → revoked becomes
  a timeline an attacker can reconstruct.

At the same time, clients need to react correctly: a `401` should trigger a refresh-and-retry flow,
not a logout loop. The mechanism for "please refresh" must not leak token state to an attacker who is
not the legitimate client.

## The internal event space

| Internal event | Meaning | External response |
| -------------- | ------- | ----------------- |
| Session expired (idle/absolute) | Time-based | `401 UNAUTHENTICATED` |
| Access token expired | JWT `exp` passed | `401 UNAUTHENTICATED` |
| Refresh token expired/revoked | Cannot refresh | `401 UNAUTHENTICATED` |
| Token revoked (logout, admin) | Server-side kill | `401 UNAUTHENTICATED` |
| Token signature invalid | Tampered/forged | `401 UNAUTHENTICATED` |
| Token audience/issuer mismatch | Wrong environment/service | `401 UNAUTHENTICATED` |
| User deleted/deactivated | Account gone | `401 UNAUTHENTICATED` |

All seven → the **same** external shape. Only the internal audit record and metric label differ.

## How it works (mechanics)

```text
 request ──▶ auth middleware
                │
                ├─ no token ──────────────────────▶ 401 (missing)
                │
                └─ token present ──▶ verify()
                        │
                        ├─ signature/claims fail ──▶ 401 (reason: invalid)
                        ├─ exp passed ─────────────▶ 401 (reason: expired)
                        ├─ jti in revocation list ─▶ 401 (reason: revoked)
                        └─ valid ──────────────────▶ continue
                        │
             (all failures share one external body + challenge)
```

The decision to "refresh and retry" is driven by the **client's own knowledge** that it holds a
refresh token, not by a distinct server code. A properly designed client attempts refresh on any
`401`, and the server's refresh endpoint enforces its own validity.

## Worked example — silent distinction

```ts
// ❌ Leaks token lifecycle to the client.
if (jwtExpired(token))   return res.status(401).json({ code: "TOKEN_EXPIRED" });
if (isRevoked(jti))      return res.status(401).json({ code: "TOKEN_REVOKED" });

// ✅ One external shape; internal reason for operators.
const result = verifyAccessToken(token); // -> { ok:true, principal } | { ok:false, reason }

if (!result.ok) {
  log.info(
    { event: "auth_failed", requestId: req.id, reason: result.reason }, // internal only
    "access token rejected",
  );
  metrics.increment("auth_failed_total", { reason: result.reason }); // bounded label
  res.setHeader("WWW-Authenticate", 'Bearer realm="api", error="invalid_token"');
  return res.status(401).json({ code: "UNAUTHENTICATED", message: "Authentication required." });
}

req.principal = result.principal;
```

The `reason` values (`invalid`, `expired`, `revoked`, `audience`) are safe as **metric labels**
(bounded set, no per-user data) but must never be returned.

## Revocation mechanics that affect errors

| Mechanism | Error interaction |
| --------- | ----------------- |
| Denylist (`jti` in Redis with TTL) | Denylist outage must **fail closed** (treat as revoked or reject) |
| Token version / `iat` cutoff | A bumped cutoff invalidates all older tokens — same external `401` |
| Short-lived access + refresh | Prefer this; fewer revocation edge cases |
| Session store lookup | Store outage → `503`, not `401` (see below) |

> ⚠️ **Hazard.** If the revocation store is unavailable, the safe answer for a *revocation-aware*
> service is to reject the token (fail closed) — not to accept it "optimistically". Accepting on
> error is a fail-open bypass for exactly the tokens you were trying to kill.

### 401 vs 503 when the auth store is down

If you cannot determine token validity because a *dependency* is down, and you cannot fail closed
cheaply, return **`503 Service Unavailable`** rather than `401`. A `401` falsely tells the client its
credentials are bad and can trigger a mass logout/refresh storm. A `503` says "try again". The choice
depends on whether you can safely deny: for high-risk operations, deny (`401`/`403`); for
availability-critical ones, `503` with `Retry-After` is often better than a wrong `401`.

## Key data / numbers

- **RFC 6750**: `WWW-Authenticate: Bearer error="invalid_token"` is the standard challenge for any
  invalid token, regardless of sub-reason.
- **OWASP A07** and the JWT guidance recommend short-lived access tokens (commonly 5–15 min) plus
  refresh tokens, specifically to reduce revocation complexity.
- **CWE-613: Insufficient Session Expiration** — sessions that do not expire are the weakness this
  section prevents; the *error* side is about not over-communicating expiry.
- **`503` + `Retry-After`** is the correct signal for a transient auth-dependency outage where denial
  is not required.

## Real-world use case — Acme SaaS

Acme returned `TOKEN_REVOKED` when a user's session was killed by an admin. Two problems surfaced:
(1) attackers used the distinct code to confirm which stolen tokens had been detected and revoked,
and (2) a buggy mobile client logged users out permanently on `TOKEN_REVOKED` but attempted refresh on
`TOKEN_EXPIRED`, so the two codes drove inconsistent client behavior. Fix: both became
`UNAUTHENTICATED`; the mobile client now attempts refresh on any `401` and only logs out when refresh
itself fails. Revocation detection is now invisible externally, and client behavior is uniform.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single `UNAUTHENTICATED` | No lifecycle leak | Clients must generalize refresh | Default |
| Distinct expired/revoked codes | Explicit client handling | Leaks lifecycle/incident state | Never for public APIs |
| `503` on auth-store outage | Preserves availability, avoids false logout | Client must retry | Non-denial-required paths |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return one `401` for all token-state failures | Expose `TOKEN_REVOKED`/`TOKEN_EXPIRED` |
| Keep refresh-token state private | Tell the client whether a token was once valid |
| Fail closed when the denylist is down | Accept tokens on denylist error |
| Use `503` when validity is unknown but denial is not required | Return a false `401` |
| Prefer short-lived access + refresh | Rely on long-lived tokens you must revoke |

## Common mistakes

- **Distinct expired vs revoked codes.** Leaks incident state.
- **Fail-open revocation.** Accepts exactly the tokens you tried to kill.
- **`401` for a dependency outage.** Triggers logout storms; prefer `503`.
- **Refresh endpoint that itself leaks.** The refresh error must also be uniform.
- **Logging the raw token or `jti` at info level.** The `jti` is fine internally; the token is not.

## Checklist

- [ ] Do expired, revoked, invalid, and deleted-account all return one `401` shape?
- [ ] Is the internal reason logged and metric-labeled but never returned?
- [ ] Does the denylist fail **closed**?
- [ ] Is a dependency outage `503`, not a false `401`?
- [ ] Does the refresh endpoint return a uniform error too?
- [ ] Are tokens/`jti` handled per the redaction strategy?

## Related

- [Missing and Invalid Credentials](./01-missing-and-invalid-credentials.md)
- [Existence Disclosure and Consistent Status](./05-existence-disclosure-and-consistent-status.md)
- [Deep dive: Identity Provider and Policy Engine Failures](../02-deep-dive/03-identity-provider-and-policy-engine-failures.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Glossary](../../../GLOSSARY.md)
