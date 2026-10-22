# Fail-Open vs Fail-Closed

> Part XI · Chapter 30 · Sections 30.10–30.15 · _Estimated reading time: 23 min_
> **Prerequisite:** [Fail-Closed vs Fail-Open, Cascades, and Eligibility](../01-concepts/05-fail-closed-vs-open-and-cascading.md)

## In one sentence

Fail-open and fail-closed are **risk allocations**, not availability settings: each one chooses which
kind of failure you are willing to have, so the decision must be derived from the cost of being wrong
rather than from a library default.

## Why this matters in production

Every failure path makes an implicit choice. If an authorization service times out and the request
proceeds, you chose fail-open — possibly without knowing. If a feature flag service is unreachable and
every optional feature disappears, you chose fail-closed for all of them. These choices surface in
incidents and audits. A written framework makes them deliberate, consistent, and defensible, and it
keeps a well-meaning "improve availability" change from quietly weakening security.

## The four dimensions

Evaluate each capability on four questions:

### 1. Correctness cost

If the operation proceeds without the check/source, is the result still *true*?

```text
proceed → correct?  → fail-open candidate
proceed → wrong?    → fail-closed
```

### 2. Safety and security cost

Can proceeding cause harm — unauthorized access, financial loss, data corruption, legal exposure?

```text
harm possible → fail-closed (or human review)
harm impossible → fail-open candidate
```

### 3. Reversibility

If you allow the operation, can it be undone or reconciled?

| Reversibility | Leaning |
| ------------- | ------- |
| Fully reversible (read) | Fail-open |
| Compensatable (queued email) | Fail-open with retry |
| Partially reversible (reservation) | Fail-closed |
| Irreversible (charge, delete, send) | Fail-closed |

### 4. Observability and detectability

Will you know the fallback happened? Fail-open is only tolerable when it is **counted and alerted**.
Invisible fail-open is silent inaccuracy.

```text
fail-open + metric + alert  → acceptable
fail-open + no signal       → unacceptable
```

## The decision procedure

```text
1. Is the operation a read or a write?
   write with side effects → fail-closed unless idempotent + compensatable

2. Can proceeding produce an incorrect or unsafe result?
   yes → fail-closed

3. Is the effect irreversible?
   yes → fail-closed

4. Is the dependency required by contract/regulation?
   yes → fail-closed

5. Will we detect and count the fallback?
   no → fail-closed or add instrumentation first

6. Otherwise → fail-open, with a labelled degraded result
```

### Scoring table

| Capability | Correctness | Safety | Reversible | Detectable | Decision |
| ---------- | :---------: | :----: | :--------: | :--------: | -------- |
| Recommend products | low cost | none | yes | yes | Open |
| Show usage chart | low | none | yes | yes | Open |
| Send receipt email | none | none | queued | yes | Open (queue) |
| Search ranking | medium | none | yes | yes | Open (keyword) |
| Tax estimate (display) | medium | low | yes | yes | Open (labelled) |
| Tax charge | high | high | no | yes | Closed |
| Payment authorization | high | high | no | yes | Closed |
| Permission check | high | high | no | yes | Closed |
| Session validation | high | high | no | yes | Closed |
| Inventory reservation | high | medium | partial | yes | Closed |
| Idempotency check | high | high | no | yes | Closed |
| Rate limiting | medium | medium | yes | yes | Open with local fallback |
| Audit logging | high (compliance) | high | no | yes | Closed for audited actions |

## Why "fail-safe" is ambiguous

Some literature uses *fail-safe* to mean "fail to the safe state," which may be open or closed depending
on the system:

| System | Safe state |
| ------ | ---------- |
| Elevator brake | Closed (stop) |
| Door lock | Closed (locked) |
| Authentication | Closed (deny) |
| Recommendation widget | Open (hide) |
| Analytics pipeline | Open (drop) |

Do not use "fail-safe" without saying which state is safe. In this book: **fail-closed = deny**,
**fail-open = allow**.

## Interaction with retries and breakers

The mode determines what happens *after* retries and the breaker have given up.

```text
retry exhausted / breaker open
        │
        ├─ fail-closed → 503 + Retry-After (no substitute)
        │
        └─ fail-open   → substitute (cached, derived, static) with provenance
                         └─ if substitute also fails → terminal 503
```

Important: fail-open does **not** mean "retry forever." It means "serve a correct substitute." If no
correct substitute exists, fail-open collapses back to fail-closed.

### Breaker mode implications

| Breaker consumer | Fail-closed breaker | Fail-open breaker |
| ---------------- | ------------------- | ----------------- |
| Payments | Reject requests | **Never** — would allow unpaid orders |
| Recommendations | Empty page | Serve popular items |
| Search | Error page | Keyword results |
| Rate limiter | Reject all traffic | Local limit |
| Feature flags | All flags off | Last-known flags |

A "fail-open breaker" is just a breaker whose open state returns a substitute instead of an error.

## Security-shaped failure modes

Fail-open choices are where resilience and security collide.

| Check | Fail-open consequence |
| ----- | --------------------- |
| Auth token validation | Unauthenticated access |
| Authorization | Privilege escalation |
| Tenant isolation | Cross-tenant data leak |
| Revocation check | Revoked sessions stay valid |
| Fraud scoring | Fraudulent charges |
| Rate limiting | Abuse, resource exhaustion |
| Audit log write | Missing compliance evidence |
| Input validation | Injection, corruption |

**Rule:** a check that exists to *prevent* something must fail closed. A check that exists to
*optimize* something may fail open.

## Worked example — feature flag service outage

```text
Flag service unavailable.
Option A (fail-open to "all features on"):
  - risky features turn on for everyone
  - experiments activate unexpectedly
Option B (fail-closed to "all features off"):
  - checkout button hidden behind a flag → outage
Option C (fail to last-known cached flags):
  - behavior unchanged for up to TTL
  - clearly documented, predictable
```

Acme chose **C**: the flag SDK caches last-known values with a 5-minute TTL and a local file fallback.
When the flag service is down, `flags.lastUpdated` is surfaced in the admin UI, and a metric
`flag_cache_used_total` fires. This is neither pure fail-open nor pure fail-closed; it is "fail to the
last deliberate configuration."

The lesson: the best answer is often a **third state** (last-known, local limit, cached value), not a
binary.

## Worked example — authorization outage

```text
Permission service p99 80ms → times out at 500ms.
Correct behavior: deny the request (fail-closed), return 503.
Bad behavior: allow because "the user was probably fine."
Worse behavior: use a stale permission cache with a 30s TTL for cross-tenant checks.
```

Acme's final design:

- Permission checks: fail-closed against the primary with a 500ms timeout.
- A **local 5s** cache for the same user's own permissions only (reduces load, bounds staleness).
- Cross-tenant/admin checks: no cache, fail-closed.
- 503 responses include `Retry-After: 2` and an error code `AUTHZ_UNAVAILABLE`.

## Worked example — audit logging

Audit is a write with compliance consequences. If the audit sink is unavailable:

| Approach | Verdict |
| -------- | ------- |
| Proceed without audit | ❌ Compliance violation |
| Fail the business action | ✅ For audited actions |
| Buffer locally and ack later | ⚠️ Only if durable + replayable |

Acme buffers audit records to a local durable queue for up to 60s; if the buffer is full, the audited
action fails closed. This preserves both compliance and availability for short outages.

## Documenting the decision

```yaml
capability: tax_charge
mode: fail_closed
rationale: "Incorrect tax is a financial/legal liability and irreversible."
fallback: none
error: { status: 503, code: TAX_UNAVAILABLE, retry_after_s: 5 }
owner: payments
reviewed: 2026-10-01
```

Every capability should have this record. Review it when:

- the dependency's SLA changes,
- a new regulator/contract adds freshness requirements,
- an incident shows the choice was wrong,
- a product change alters the cost of being wrong.

## Key data / numbers

- Decision dimensions: **4** (correctness, safety, reversibility, detectability).
- Flag cache TTL: **5 minutes**, last-known values.
- Permission check timeout: **500ms**, fail-closed.
- Local permission cache: **5s**, same-user only.
- Rate limiter fallback: **40–50%** of normal limit.
- Audit buffer: **60s** durable, then fail closed.

## Real-world use case — Acme SaaS

Acme's API gateway failed open on its rate limiter during a Redis incident. A single misbehaving
tenant sent 40× normal traffic and saturated the database. The postmortem kept fail-open (rejecting all
traffic would have been worse) but added a local token bucket at 40% of the normal limit, per-tenant
caps, and an alert when the limiter store was unavailable. A repeat incident produced a 2× traffic
increase instead of 40×, and no database saturation.

## Trade-offs

| Mode | Availability | Correctness | Security | Operational clarity |
| ---- | :----------: | :---------: | :------: | :-----------------: |
| Fail-closed | Low | High | High | High |
| Fail-open | High | Low–Medium | Low | Medium |
| Last-known | High | Medium | Medium | High |
| Local fallback | High | Medium | Medium–High | Medium |
| Human review | Medium | High | High | Low |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide per capability, in writing | Use one global default |
| Fail closed for prevention checks | Fail open on authorization |
| Detect and count every fail-open | Allow invisible fallbacks |
| Prefer last-known/local states | Assume a binary choice |
| Review after incidents and changes | Set it once and forget |
| Name the safe state explicitly | Say "fail-safe" ambiguously |

## Common mistakes

- **Fail-open authorization** introduced as an "availability fix."
- **Fail-closed optional features**, turning a widget outage into a page outage.
- **No instrumentation**, so fail-open is invisible.
- **Stale security caches** treated as availability wins.
- **Binary thinking**, missing the last-known or local-limit option.

## Checklist

- [ ] Every capability records mode, rationale, owner, and review date.
- [ ] Prevention checks (auth, authz, validation) fail closed.
- [ ] Optional features fail open with a labelled substitute.
- [ ] Irreversible operations fail closed or compensate.
- [ ] Fail-open paths are counted and alerted.
- [ ] Last-known/local fallbacks are preferred over guessing.
- [ ] Decisions are reviewed after incidents and product changes.

## Related

- [Fail-Closed vs Fail-Open, Cascades, and Eligibility](../01-concepts/05-fail-closed-vs-open-and-cascading.md)
- [Fallback Chains](./01-fallback-chains.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
