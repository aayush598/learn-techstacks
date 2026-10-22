# Account Lifecycle Errors — Sign-up, Verification, Reset, Sessions

> Part XVI · Chapter 42 · Sections 42.1–42.4 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)

## In one sentence

Every account-lifecycle step — sign-up, email verification, password reset, session refresh —
is a **small state machine with an enumeration-safe error contract**, and the failures that
hurt are the ones caused by races and retries, not by wrong input.

## Why this matters in production

These endpoints sit at the front door of the product, so they are hit by bots, raced by
double-clicks, and retried by flaky mobile networks. Getting them wrong has three concrete
costs: **duplicate accounts** (one user, two identities, split billing), **support load**
("I never got the reset email"), and **security incidents** (user enumeration, refresh-token
reuse that never gets detected). Each subsection below names the failure, the correct outcome,
and the error contract.

## 42.1 — Sign-up and account creation

The happy path is one INSERT. Production adds three failure modes:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Duplicate email | User retries; concurrent submits | Treat unique-violation as "already registered" → verification/resend flow, **not** a 500 |
| Tenant/slug collision | Two orgs pick `acme` | Deterministic suffix or 409 with field-level error; never overwrite |
| Welcome email fails | Provider outage | **Account still created**; email enqueued for retry; surface "verify later" state |

The critical rule: **never make the external email provider part of the account-creation
transaction.** Create the row, commit, then enqueue the email. If the email fails, the user
exists and can resend; if you couple them, an email outage means lost sign-ups.

```ts
// Race-safe sign-up: the unique constraint IS the duplicate detector.
async function signUp(input: SignUpInput): Promise<Result<AccountId, SignUpError>> {
  const passwordHash = await hashPassword(input.password); // before the tx, it is slow
  try {
    const id = await db.insert("users", {
      email: input.email.toLowerCase(), // normalize before comparing
      password_hash: passwordHash,
      email_verified_at: null,
    });                                   // UNIQUE (email)
    await outbox.enqueue({ type: "user.signup", accountId: id, email: input.email });
    return Ok(id);
  } catch (err) {
    if (isUniqueViolation(err, "users_email_key")) {
      // Do NOT reveal "this email is taken" on a public sign-up if your threat model
      // requires enumeration resistance; route to the resend-verification flow instead.
      return Err(EmailAlreadyRegistered); // or GenericAccepted, see trade-offs
    }
    throw err;                            // anything else is not a business outcome
  }
}
```

**Key data:** `SQLSTATE 23505` (unique_violation) is the signal, not a string match on the
message. Email tokens are single-use with a TTL commonly of **24 hours**. Normalization
(lowercase, trim) before the uniqueness check prevents "A@x.com" vs "a@x.com" duplicates.

## 42.2 — Email verification

Verification failures are almost always **token lifecycle** failures:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Unknown token | Typo, already used, truncated link | Generic invalid-link page + resend CTA; never a 500 |
| Expired token | User waited days | "Expired — request a new one"; do not extend silently |
| Token replayed | Link clicked twice / prefetcher | Second use: treat as already-verified (idempotent success), not an error |
| Resend abuse | User hammers resend | Per-account + per-IP rate limit; generic 202 response |

Store a **hash** of the token, not the token — a leaked DB dump must not allow verification
emails to be forged. Verification itself is idempotent: `UPDATE ... SET email_verified_at =
COALESCE(email_verified_at, now())`.

> ⚠️ **Hazard.** Email link prefetchers (security scanners, mail clients) will "click" your
> verification URL. If clicking once consumes the token and the user then clicks it for real,
> they see a confusing error. Make the second click a success.

## 42.3 — Password reset

The reset endpoint is the classic **user-enumeration** trap:

```text
POST /password-reset
  → always 202 Accepted, identical body, identical timing class
  → if account exists: enqueue reset email (single-use token, TTL commonly 30–60 min)
  → if not:            enqueue nothing, still 202
```

Rules that must hold:

1. **Same response** for existing and non-existing accounts (status, body, approximate timing).
2. Token single-use; hashed at rest; invalidated on password change ("log out all devices").
3. Resend throttled per account and per IP — otherwise the endpoint is an email-bomb vector.
4. Never put the token in a query parameter that ends up in proxy logs if you can avoid it;
   if you must, treat the link as a bearer secret and make it single-use anyway.

Reset *confirmation* (`POST /password-reset/confirm`) is where real errors surface: token
expired, token unknown, password too weak, token already used. These are **user-actionable
4xx**, never 5xx.

## 42.4 — Session create and refresh

Session failures are the ones users feel as "it logged me out" or, worse, as a security hole
that never logs anyone out:

| Failure | Cause | Correct outcome |
| ------- | ----- | --------------- |
| Access token expired | Short TTL | `401` + error code the client uses to trigger refresh — not a generic 401 that kills the UI |
| Refresh token expired/revoked | Long idle, logout, rotation | `401` terminal → full re-auth |
| **Refresh token reuse** | Stolen token or buggy client | **Revoke the whole token family**; force re-auth; alert |
| Concurrent refresh (multi-device) | Two tabs refresh at once | Grace window accepting the immediately-previous token, or lock-protected rotation |
| Clock skew | Server/leaser drift | Accept small negative leeway (commonly ~30–60 s) on expiry checks |

Refresh-token **rotation** (issue a new refresh token on every use) plus **reuse detection**
(store a hash of the current token; any older hash appearing means theft) is the standard
defensive design. The failure mode it prevents: a stolen refresh token being valid forever
because rotation was never implemented.

```ts
async function refresh(rawRefreshToken: string): Promise<Result<Session, RefreshError>> {
  const presented = sha256(rawRefreshToken);
  const family = await tokenFamilies.findByHash(presented); // lookup by hash
  if (!family) return Err(InvalidRefreshToken);             // unknown → terminal

  if (family.currentHash !== presented) {
    // A rotated-out token came back: theft or a zombie client. Fail closed.
    await tokenFamilies.revokeAll(family.id);
    audit.append({ event: "refresh_reuse_detected", familyId: family.id });
    return Err(RefreshReuseDetected);                       // terminal, force re-auth
  }

  const session = await rotate(family);                     // new access + refresh
  return Ok(session);
}
```

**Key data:** access-token TTL commonly **15 minutes**; refresh-token rotation on every use;
reuse ⇒ revoke family; `401` with a machine-readable code (e.g. `AUTH_TOKEN_EXPIRED` vs
`AUTH_REFRESH_INVALID`) so clients can distinguish "refresh" from "re-auth".

## Worked example — Acme SaaS sign-up burst

Acme ran a Product Hunt launch. Two problems surfaced within an hour: (1) users who double-
clicked "Create account" got `500`s because the duplicate INSERT threw past the handler — the
fix was catching `23505` and returning the resend-verification flow; (2) the welcome-email
worker was down, and because email sending was inline in the sign-up transaction, **every
sign-up failed entirely**. Moving the email to the outbox pattern turned an email outage into
"a few delayed welcome emails." Both bugs were in the account lifecycle, both were retries and
coupling, neither was "an exception-handling bug" in the classical sense.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Reveal "email taken" on sign-up | Better UX | Enables enumeration | Apps where accounts are not secret |
| Generic accepted on sign-up | Enumeration-resistant | Confusing for real users | Public SaaS, security-sensitive |
| Grace window on refresh | Multi-device friendly | Slightly larger theft window | Consumer apps with many devices |
| Strict rotation, no grace | Strongest theft detection | Occasional spurious logout | B2B / high-security |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Detect duplicates via unique constraint (`23505`) | SELECT-then-INSERT (races lose) |
| Commit the account, then enqueue the email | Send email inside the DB transaction |
| Answer reset requests identically for known/unknown emails | Return 404 for unknown accounts |
| Hash reset/verification tokens at rest | Store raw tokens |
| Revoke the token family on refresh reuse | Log the reuse and continue |
| Give clients distinct codes for expired vs invalid refresh | Return a bare `401` |

## Common mistakes

- **SELECT-then-INSERT sign-up** — two concurrent requests both pass the check; one dies on
  the constraint with a 500. Catch `23505` instead.
- **Reset token in the URL with a long TTL and reuse allowed** — a leaked link is a takeover.
- **Single global rate limit on reset** — one attacker's hammering locks out a real user;
  limit per account *and* per IP.
- **`401` with no code** — clients cannot tell whether to refresh or re-authenticate, so they
  re-auth always and users get logged out on every token expiry.
- **No reuse detection** — a stolen refresh token stays valid for months.

## Checklist

- [ ] Sign-up handles `23505` as a business outcome, not an exception.
- [ ] Account creation does not depend on the email provider being up.
- [ ] Verification/reset tokens are hashed, single-use, and TTL-bounded.
- [ ] Password-reset responses do not disclose account existence.
- [ ] Resend endpoints are rate-limited per account and per IP.
- [ ] Refresh tokens rotate, and reuse revokes the family.
- [ ] Client-facing auth errors carry machine-readable codes.

## Related

- [Subscription and Payment Errors](./02-subscription-and-payment-errors.md)
- [Ambiguous Payment Outcomes and Idempotency](../02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md)
- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
