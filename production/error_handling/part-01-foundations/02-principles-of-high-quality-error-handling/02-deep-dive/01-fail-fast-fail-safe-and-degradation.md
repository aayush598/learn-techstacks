# Fail-Fast, Fail-Safe, and Degradation — A Decision Framework

> Part I · Chapter 2 · Sections 2.7–2.9 · _Estimated reading time: 20 min_

## In one sentence

Choosing between **fail-fast**, **fail-safe**, and **graceful degradation** is a per-operation
decision driven by three questions — *is it recoverable, is it critical, and is it a
security/integrity decision?* — and it must be made on purpose, then written down.

## Why this matters in production

A single wrong posture can dominate your reliability. Fail-fast on a cosmetic dependency causes
avoidable outages; degrade a payment path and you lose money; fail-open an authorization check and
you leak data. Posture errors are high-impact precisely because they turn a local failure into a
global consequence.

This deep dive gives you a repeatable way to pick the posture and to spot when a system has mixed
postures inconsistently.

## Core concept — the three postures

| Posture | On failure | Protects | Sacrifices | Typical owner of decision |
| ------- | ---------- | -------- | ---------- | ------------------------- |
| **Fail-fast** | Stop now, surface the error | Correctness, no corrupt state | Availability | Engineer/domain |
| **Fail-safe** | Continue in a safe, restricted state (usually deny) | Security, integrity | Availability/function | Security/product |
| **Degrade** | Continue with reduced, honest functionality | Availability | Completeness/freshness | Product |

Fail-fast and fail-safe both *abort the current operation*; they differ in what "safe" means.
Degradation is the only one that *continues* the operation, with reduced behavior.

## How it works (mechanics) — the decision tree

```text
                    ┌─────────────────────────────┐
                    │ Does continuing risk         │
                    │ security or data integrity?  │
                    └───────────────┬──────────────┘
                       yes │                    │ no
                           ▼                    ▼
                     FAIL-SAFE            ┌───────────────────────┐
                     (deny / block)       │ Is the failure         │
                                          │ recoverable (transient,│
                                          │ idempotent)?           │
                                          └──────────┬────────────┘
                                             yes │         │ no
                                                 ▼         ▼
                                        RETRY then      ┌────────────────────┐
                                        re-evaluate     │ Is the feature      │
                                                        │ optional?           │
                                                        └─────────┬──────────┘
                                                          yes │        │ no
                                                              ▼        ▼
                                                          DEGRADE    FAIL-FAST
                                                          (honest)   (5xx)
```

Order matters: **security/integrity is checked first**. You never degrade or fail-fast your way out
of a security decision.

## The three questions, applied

### 1. Is it recoverable?

- **Transient + idempotent** (`429`, `503`, `40001`, timeout) → retry (Chapter 27), then re-evaluate.
- **Permanent** (`422`, `404`, card declined) → do not retry; map to the correct outcome.

### 2. Is it critical?

- **Critical dependency** (payments to charge, primary DB to read) → fail-fast with `503`.
- **Optional dependency** (recommendations, avatars, telemetry) → degrade.

### 3. Is it a security/integrity decision?

- Authz check, signature verification, balance check, payout eligibility → **fail-safe**. Always.

## Edge cases

| Situation | Naive choice | Correct posture | Why |
| --------- | ------------ | --------------- | --- |
| Authz service times out | fail-open (allow) | **fail-safe** (deny) | Never allow on uncertainty |
| Fraud score unavailable | fail-fast (reject order) | **degrade + manual review** | Don't block revenue, don't auto-approve risk |
| Avatar CDN down | fail-fast (500 page) | **degrade** (placeholder) | Cosmetic |
| Config missing at boot | degrade (start anyway) | **fail-fast** (refuse to start) | Running with unknown config is worse |
| Read replica lag | error | **serve fresh primary / mark stale** | Freshness is a contract (Chapter 30) |
| Partial batch write | mark all failed | **record per-item** | Partial failure is real (Chapter 39) |

## Worked example — posture matrix for one request

**Acme SaaS** dashboard request touches four dependencies with four different postures:

```text
  request → [ auth ]──────────── fail-safe (deny) ────────┐  critical, security
          → [ projects DB ]───── fail-fast (503) ─────────┤  critical
          → [ activity feed ]─── degrade (cached) ────────┤  optional, freshness-flagged
          → [ LLM summary ]───── degrade (placeholder) ───┘  optional
```

```ts
async function getDashboard(userId: string) {
  const principal = await auth.authorize(userId);          // throws → fail-safe (401/403)
  const projects = await projectsRepo.list(principal);     // throws → fail-fast (503)
  let feed: Activity[] = [];
  try { feed = await activityFeed.list(principal); }
  catch (err) { log.warn({ err }, "feed degraded"); feed = cachedFeed(principal); }
  let summary: string | null = null;
  try { summary = await llm.summarize(principal); }
  catch (err) { log.warn({ err }, "summary degraded"); }   // null → placeholder in UI
  return { projects, feed, summary, degraded: { feed: feed.length === 0 } };
}
```

Same endpoint, four deliberate postures.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Maintenance/unavailable | `503` | Set `Retry-After` when a retry is sensible |
| Upstream timeout | `504` | Client-side deadline exceeded |
| Too many requests | `429` | Include `Retry-After` |
| Circuit breaker threshold | commonly 5 consecutive failures | Then open; half-open after cooldown |
| Half-open probe | 1–3 trial requests | Close on success, reopen on failure |
| Deny on authz failure | `403` | Fail-safe result |
| Auth failure | `401` | Missing/invalid credentials |

## Real-world use case — Acme SaaS

Acme's auth middleware originally **failed open** when the permission service timed out, to "avoid
locking users out." A permission-service incident turned into a cross-tenant data exposure because
requests were allowed when authorization could not be evaluated. The team flipped the default to
**fail-safe** (deny with `403` and a clear code) and added a fast local cache of decisions with a
short TTL so ordinary traffic was unaffected. Availability dipped 0.1% during that incident;
integrity risk went to zero. Posture was the entire fix.

## Trade-offs

| Posture | Availability | Safety | Complexity | Choose when |
| ------- | ------------ | ------ | ---------- | ----------- |
| Fail-fast | Lower | High | Low | Critical deps, bugs, invariants |
| Fail-safe | Lower | Highest | Medium | Security, integrity, money |
| Degrade | Highest | Medium | Highest (fallbacks) | Optional features, read paths |
| Fail-open | Highest | Lowest | Low | Rare, documented, reversible |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide posture per operation, in writing | Inherit one posture for the whole service |
| Check integrity/security first | Degrade or fail-fast a security decision |
| Make degradation honest (flag stale) | Present degraded data as authoritative |
| Fail-fast at boot on bad config | Start with unknown configuration |

## Common mistakes

- **One posture everywhere** — "we always retry" or "we always degrade."
- **Downgrading a security failure to availability** — the classic fail-open mistake.
- **Confusing retry with posture** — retry is a *recovery*, posture is the *outcome if it fails*.
- **Undocumented degradation** — users cannot tell the feature is stale.

## Checklist

- [ ] Is each fallible dependency assigned exactly one posture?
- [ ] Are security/integrity decisions fail-safe?
- [ ] Does every degradation have an honest fallback (and a signal)?
- [ ] Is fail-open used anywhere, and is it deliberate and documented?
- [ ] Does boot config fail-fast on missing required values?

## Related

- [Failure Posture and Defensive Design](../01-concepts/03-failure-posture-and-defensive-design.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Glossary: fail-closed / fail-open](../../../GLOSSARY.md)
