# Chapter 50 — Reference

> Part XIX · Chapter 50 · Rule catalogue, templates, decision tables, and glossary.

## Cheat sheet — the standard file

```yaml
standard:
  id: acme-error-handling
  version: 1.4.0
  owner: platform-guild
  reviewed_on: 2026-04-02        # quarterly
  rules: 41                      # budget: 30–50, new orgs start at 12–15
```

## Cheat sheet — a rule row

```text
id · normative statement · applies-to · checked-by · reason · exception
```

| Field | Required | Example |
| ----- | -------- | ------- |
| `id` | Yes | `R-RETRY-2` |
| statement | Yes | "Every retry call site MUST use a policy from the shared registry" |
| applies-to | Yes | `all services`, or `public surfaces` |
| checked-by | Yes | `CI retry-policy-lint` |
| reason | Yes | "three teams each implemented their own backoff" |
| exception | Yes | `yes — EX-019`, or `no (security floor)` |

## Rule catalogue index

| Prefix | Area | Rules | Enforced by |
| ------ | ---- | ----- | ----------- |
| `R-NAME-*` | Naming and codes | 6 | CI registry check + review |
| `R-STRUCT-*` | Code shape and module layout | 5 | CI import lint + review |
| `R-PROP-*` | Propagation and translation | 6 | CI lint + review |
| `R-RETRY-*` | Retry and timeout | 6 | CI retry-policy lint |
| `R-RESP-*` | Response format and status codes | 8 | CI response snapshot + review |
| `R-RECOV-*` | Recovery posture | 6 | CI policy lint + review |
| `R-SEC-*` | Security floor (non-exceptable) | 15 | CI redaction check + security review |

## Decision table — choosing an HTTP status

| Situation | Status | Retryable | Rule |
| --------- | ------ | --------- | ---- |
| Malformed or invalid input | `400` | No | `R-RESP-4` |
| Missing or invalid credentials | `401` | No | `R-SEC-7` |
| Absent *or* invisible resource | `404` | No | `R-RESP-3` |
| Duplicate or state conflict | `409` | No | `R-RESP-4` |
| Well-formed but semantically invalid | `422` | No | `R-RESP-6` |
| Throttled | `429` + `Retry-After` | Yes, after the delay | `R-RESP-5` |
| Unexpected server bug | `500` | Yes | `R-RESP-4` |
| Dependency unavailable, transient | `503` | Yes | `R-RETRY-1` |
| Timeout on a dependency | `504` | Yes | `R-RECOV-2` |

## Decision table — SQLSTATE class → behaviour

| Class | Meaning | Category | Retryable |
| ----- | ------- | -------- | --------- |
| `08` | Connection exception | transient | Yes |
| `23` | Integrity constraint violation (`23505` unique) | permanent | No |
| `40` | Transaction rollback, `40001` serialization failure | transient | Yes, after rollback |
| `42` | Syntax error or access rule violation | permanent | No |
| `53` | Insufficient resources | transient | Yes, bounded |

## Decision table — error category → recovery

| Category | Example | Recovery | Status |
| -------- | ------- | -------- | ------ |
| Validation | `FIELD_INVALID` | Fix the request; return field details | `422` |
| Conflict | `DUPLICATE_ORDER` | Caller resolves; keep the idempotency key | `409` |
| Authorization | `TENANT_FORBIDDEN` | Fail closed; never leak existence | `403` |
| Dependency (transient) | `TIMEOUT`, `SQLSTATE 08` | Retry within budget, then `503` | `503` |
| Dependency (permanent) | `SQLSTATE 42` | Fail closed; no retry | `502`/`500` |
| Partial | `SHIPMENT_LABEL_FAILED` | Return partial state, compensate | `200` with a partial marker |
| Bug | `UNEXPECTED` | Alert, fail closed, no retry at the caller | `500` |

## Cheat sheet — retry policy

```yaml
# standards/error-handling/retry-policies.yaml
policies:
  - id: RP-DEFAULT
    maxAttempts: 3
    baseDelayMs: 100
    backoff: exponential          # exponential | constant
    jitter: full                  # full | equal | none
    totalDeadlineMs: 3000
    eligibleCodes: [TIMEOUT, DEPENDENCY_UNAVAILABLE, SQLSTATE_08]
    idempotencyRequired: true
```

| Field | Ceiling | Note |
| ----- | ------- | ---- |
| `maxAttempts` | ≤ 5 | CI rejects a literal count above 5 |
| `totalDeadlineMs` | ≤ 30000 on a sync surface | Must fit inside the caller's budget |
| Retry budget | ≤ 10% of the request deadline | Prevents retries from owning the latency |
| Backoff | exponential + jitter | Constant delays synchronise the herd |
| Idempotency | required | Or the call must carry an idempotency key |

## Cheat sheet — the exceptions register

```yaml
# standards/error-handling/exceptions.yaml
exceptions:
  - id: EX-021
    rule: R-RETRY-1
    scope: ingest/webhook-ingest
    justification: >
      Why the rule cannot be met here, in one paragraph.
    compensating_controls:
      - what detects the problem
      - what contains the damage
    approved_by: platform-guild
    approved_on: 2026-04-02
    review_on: 2026-10-02
    expires_on: 2026-10-02
    status: active
```

**Required fields (8):** rule · scope · justification · compensating controls · approver · approval
date · review date · expiry date. **Default lifetime: 180 days.**

## Decision table — change class → version bump

| Change class | Example | Bump | Notice |
| ------------ | ------- | ---- | ------ |
| New guidance, new example | A new worked example | MINOR | Changelog |
| Tightening | A new mechanical rule, a stricter default | MINOR | **2 releases** in warning mode |
| Relaxation | A rule demoted to guidance | MINOR | Changelog |
| Removal | A retired rule | MAJOR | **90 days** |

## Cheat sheet — standard health metrics

| Metric | Healthy | Warning sign |
| ------ | ------- | ------------ |
| Mechanically enforced share of rules | ≥ 60% | below 40% — it is a document |
| Active exceptions | < 10 per 100 rules | rising quarter over quarter |
| Skip rate per rule | < 20% | a persistent outlier means the rule is wrong |
| Average exception lifetime | < 180 days | approaching expiry |

## Cheat sheet — SLO and error budget

| SLO | Error budget per month (30.4 days) | Effect on a rule change |
| --- | ---------------------------------- | ------------------------- |
| 99.9% | 43 m 49 s | a rule that burns 10% of the budget needs the SLO owner's sign-off |
| 99.99% | 4 m 23 s | every new dependency needs a budget line |

## Cheat sheet — risk framing for a rule

- **Severity:** 1 cosmetic · 5 degraded feature · 10 money or data lost.
- **Occurrence:** 1 rare · 5 weekly · 10 every call.
- **Detection:** 1 caught by a test · 5 found in review · 10 found in production.

- **Risk = severity × likelihood**, both on a 1–5 scale → **1** to **25**.
- **RPN = severity × occurrence × detection**, each 1–10 → **1** to **1000**.
- RPN ≥ **200**: the rule needs a named owner. RPN ≥ **400**: the rule blocks the release.

## Glossary

| Term | Meaning in this chapter |
| ---- | ----------------------- |
| **Standard** | The published set of rules, profiles, and guidance an organisation applies to error handling |
| **Rule** | A numbered, decidable statement with a check attached |
| **Guidance** | Advice that is not binding and carries no check |
| **Profile** | Per-surface parameters (timeouts, retry budgets, postures) under one guarantee set |
| **Exception** | A recorded, owned, expiring deviation from one rule in one scope |
| **Rule budget** | The maximum number of enforceable rules an organisation maintains |
| **Enforcement stage** | `off`, `warning`, or `error` — how hard a rule currently bites |
| **Security floor** | The non-exceptable rules covering disclosure, redaction, and enumeration |
| **Rule skip rate** | The share of violations or skips for one rule over a window |
| **Error budget** | The allowed share of failures inside an SLO period |

## Related

- [Chapter 50 — Error Handling as an Engineering Standard](../README.md)
- [Standards and ADR Templates](../03-practical-examples/01-standards-and-adr-templates.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 49 — Reference](../../49-error-contract-design-and-versioning/05-reference/README.md)
