# Deep Dive — Identity Provider and Policy-Engine Failures

> Part XIII · Chapter 35 · Sections 35.13–35.15 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Existence Disclosure and Consistent Status](../01-concepts/05-existence-disclosure-and-consistent-status.md)

## In one sentence

When an **identity provider** (OIDC/JWKS/introspection) or a **policy engine** fails, the safe
response is **fail closed**: deny or `503`, never accept — because availability pressure is exactly
when a fail-open fallback quietly converts an outage into an authorization bypass.

## Why this matters in production

Auth is the one subsystem where "keep the site up" instinct is most dangerous. Every fail-open
fallback reads as a reasonable availability trade-off in the incident channel and is a breach in the
postmortem. This file catalogs the specific failure points in the auth dependency chain, the correct
behavior for each, and the caching patterns that preserve *some* availability without ever granting
access that cannot be verified.

## The dependency chain

```text
 token ──▶ [ signature verify ] ──▶ [ claims/audience ] ──▶ [ session/introspection ] ──▶ principal
              │                        │                        │
           JWKS fetch              config/clock              session store
              │                        │                        │
         (IdP-hosted)            (local + NTP)            (Redis/DB)

 action ──▶ [ policy engine ] ──▶ allow/deny
              │
         (OPA/Cedar/remote PDP)
```

Each box can fail. Each failure needs a defined, fail-closed behavior.

## Failure catalog

| Failure | Symptom | Correct behavior | Wrong behavior |
| ------- | ------- | ---------------- | -------------- |
| JWKS unreachable | Cannot verify signature | Reject (`401`/`503`); use bounded-staleness cache | Accept unsigned/unverified |
| JWKS rotated, cache stale | Valid token rejected | Refresh JWKS on `kid` miss | Accept unknown `kid` |
| Introspection endpoint down | Cannot confirm token | Fail closed (`503`) | Treat as valid |
| Session store down | Cannot read session | `503` | Fabricate a session / allow |
| Clock skew | `exp`/`nbf` misfire | Allow small skew (e.g. 60 s); monitor | Disable expiry checks |
| Policy engine down | No decision | Deny + alarm | Allow |
| Policy engine slow | Timeout | Treat timeout as deny | Treat as allow |
| Config missing (issuer/aud) | Cannot validate | Fail closed at startup | Skip validation |

## JWKS caching — the one cache that is safe

Signature verification genuinely needs the IdP, but you can cache keys **with bounds**:

```ts
class JwksCache {
  private keys?: JwkSet;
  private fetchedAt = 0;
  private readonly ttlMs = 10 * 60 * 1000;      // refresh at most every 10 min
  private readonly maxStaleMs = 30 * 60 * 1000; // never trust beyond 30 min stale

  async verify(token: string): Promise<Principal | null> {
    const header = decodeHeader(token); // { kid, alg }
    let key = this.keys?.find((k) => k.kid === header.kid);

    if (!key) {
      // Unknown kid: refresh once (rotation), then fail closed if still unknown.
      await this.refresh();
      key = this.keys?.find((k) => k.kid === header.kid);
      if (!key) return null; // never accept an unverifiable signature
    }

    if (Date.now() - this.fetchedAt > this.maxStaleMs) return null; // too stale: deny
    return verifySignatureOrNull(token, key); // returns null on any failure
  }

  private async refresh() {
    try {
      const res = await fetch(`${issuer}/.well-known/jwks.json`, { timeout: 2000 });
      this.keys = await res.json();
      this.fetchedAt = Date.now();
    } catch {
      // Keep the old keys (bounded by maxStale), do not clear them.
    }
  }
}
```

Two bounds matter: **max freshness** (refresh at most) and **max staleness** (never trust too old).
Beyond staleness, deny.

> ⚠️ **Hazard.** `if (fetch fails) { validateWithoutSignature() }` is the fail-open bug. A missing
> signature verification is not "degraded auth"; it is "no auth".

## Policy engine failures

The policy engine answers `allow`/`deny`. A failure is not a decision:

```ts
async function authorize(principal: Principal, action: string, resource: Resource): Promise<boolean> {
  try {
    const decision = await policyEngine.evaluate({ principal, action, resource });
    return decision.allow;
  } catch (e) {
    metrics.increment("authz_check_error_total"); // page
    return false; // deny on any error, including timeout
  }
}
```

### Bounded-staleness decisions for low-risk reads

To preserve availability during a policy outage without an open bypass, you may cache **decisions**
for **low-risk, read-only** actions with a short TTL:

```text
Allow cached decision only if ALL hold:
  • action is read-only and low-risk (e.g. project:read)
  • decision was an explicit allow for the SAME principal + resource + action
  • TTL not exceeded (e.g. ≤ 60s)
  • tenant context unchanged
Never for: writes, financial ops, admin actions, cross-tenant access.
```

Everything else denies. A stale allow for a read is a bounded, monitored risk; a stale allow for a
write is a breach.

## Startup and configuration

| Check | On failure |
| ----- | ---------- |
| Issuer/audience configured | Fail startup |
| JWKS reachable at boot | Warn, serve but deny verification until fetched |
| Policy bundle loaded | Fail startup (never start with no policy) |
| Clock synced (NTP) | Fail startup / alarm |

Starting with auth misconfigured is worse than not starting: it serves 100% of traffic through a
weakened check.

## Key data / numbers

- **OWASP A07** and **A02: Cryptographic Failures** cover token verification failures.
- **CWE-287: Improper Authentication**, **CWE-347: Improper Verification of Cryptographic Signature**,
  **CWE-863: Incorrect Authorization**.
- **JWKS cache bounds**: commonly refresh ≤10 min, max staleness ≤30 min; refresh on unknown `kid`.
- **Clock skew tolerance**: commonly 60 s for `exp`/`nbf`; larger windows weaken replay protection.
- **Alarm**: any `authz_check_error_total` increment or `jwks_refresh_failed_total` pages on-call.

## Real-world use case — Acme SaaS

During an IdP incident, Acme's token verifier caught the JWKS fetch error and — to "stay up" — called
`jwt.decode()` instead of `jwt.verify()`, skipping signature verification for 40 minutes. Any forged
token with a plausible payload was accepted, including tokens for other tenants. Fix: unknown/unverifiable
signatures now return `null` (reject), JWKS uses the bounded cache above, a policy decision is never
cached for writes, and `jwks_refresh_failed_total` pages. The verifier's failure path now has a test
that injects a fetch error and asserts rejection. The outage behavior changed from "accept everything"
to "reject unverifiable tokens", which is the only safe option.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fail closed everywhere | No bypass | Availability dips during IdP outage | Default |
| Bounded-staleness JWKS | Verifies during brief outages | Accepts keys up to max-stale | Always (with bounds) |
| Bounded decision cache (reads only) | Some availability | Bounded stale allow | Low-risk reads only |
| Fail open | Availability | Full bypass | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reject when a signature cannot be verified | `jwt.decode()` on fetch failure |
| Bound JWKS freshness and staleness | Trust keys indefinitely |
| Deny on policy-engine error and alarm | Return allow on error |
| Cache decisions only for low-risk reads | Cache write/admin decisions |
| Fail startup on missing auth config | Start with checks disabled |

## Common mistakes

- **`decode` instead of `verify`.** The catastrophic fallback.
- **Unbounded JWKS cache.** Stale keys or infinite trust.
- **Treating policy timeout as allow.** Fail open.
- **Caching a write decision.** A stale grant for a mutation.
- **Skipping startup validation.** Serving traffic with misconfig.

## Checklist

- [ ] Does signature-verification failure reject (never accept)?
- [ ] Is the JWKS cache bounded in freshness and staleness?
- [ ] Does an unknown `kid` trigger one refresh, then deny?
- [ ] Does a policy-engine error/timeout deny and alarm?
- [ ] Are cached decisions restricted to low-risk reads with a short TTL?
- [ ] Does the app fail startup on missing auth configuration?

## Related

- [Existence Disclosure and Consistent Status](../01-concepts/05-existence-disclosure-and-consistent-status.md)
- [Session, Token Expiry, and Revocation](../01-concepts/02-session-token-expiry-and-revocation.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Glossary](../../../GLOSSARY.md)
