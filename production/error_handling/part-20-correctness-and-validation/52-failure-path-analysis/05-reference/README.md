# Chapter 52 — Reference

> Part XX · Chapter 52 · Templates, decision tables, scoring scales, and glossary.

## Cheat sheet — the failure-point list

```text
id    kind          where            note
FP-01 decision      authenticate     token verify
FP-02 interpretation validateBody    schema + fields
FP-03 effect        insertAttempt    postgres insert
FP-04 wait          chargeStripe     external call
```

Kinds: **effect** · **decision** · **boundary** · **wait** · **interpretation**.
Counts: **8–15** points per request flow, **10–20** per background job.

## Cheat sheet — the 12 guide words

| Guide word | Question | Typical mode |
| ---------- | -------- | ------------ |
| **None** | What if it does not happen at all? | The event never arrives |
| **Late** | What if it arrives late? | Timeout after the effect; stale read |
| **Early** | What if it arrives early? | Event processed before its predecessor |
| **More** | What if there are more than expected? | Duplicate delivery; fan-out |
| **Less** | What if there are fewer? | Partial batch; missing pages |
| **Wrong** | What if the content is wrong? | `200` with garbage; wrong tenant id |
| **Partial** | What if only part completes? | 3 of 5 steps committed |
| **Lost** | What if it never arrives? | Dropped message; lost ack |
| **Duplicated** | What if it arrives twice? | Two workers, same job |
| **Reversed** | What if order is inverted? | Refund before charge |
| **Corrupted** | What if the stored form is damaged? | Truncated JSON; half-written row |
| **Hung** | What if it never returns? | Deadlock; infinite await |

## Cheat sheet — the matrix row

```text
point · mode · category · recovery · maxAttempts · totalDeadline · user_sees · owner
```

## Decision table — category → recovery

| Category | Recovery | Typical status | Notes |
| -------- | -------- | -------------- | ----- |
| `validation` | fail | `422` | Return every field-level detail |
| `business` | fail | `409` | The caller's state is wrong, not the request |
| `conflict` | fail | `409` | Duplicate or illegal transition |
| `auth` | fail | `401` / `403` | Never distinguish missing from invisible |
| `external_api_permanent` | fail | `402` | A decline is not a bug; do not retry |
| `external_api_transient` | retry | `503` | ≤ 5 attempts, backoff + jitter, idempotent |
| `external_api_ambiguous` | resolve later | `202` | Read back by idempotency key; never blind retry |
| `database_transient` | retry | `503` | Roll back first; `40001` needs a new transaction |
| `data_integrity` | terminate | `500` | A constraint violation is permanent |
| `resource_exhausted` | degrade | `503` | Shed load; observe the fallback |
| `dependency_unavailable` | retry | `503` | One attempt is often enough |
| `cancellation` | fail | `499` | The client went away |
| `internal` | fail | `500` | Alert; no caller-side retry |

## Decision table — SQLSTATE class → behaviour

| Class | Meaning | Category | Recovery | Status |
| ----- | ------- | -------- | -------- | ------ |
| `08` | Connection exception | `database_transient` | retry | `503` |
| `23` | Integrity constraint (`23505` unique) | `data_integrity` | fail | `409` |
| `40` | Rollback, `40001` serialization failure | `database_transient` | retry after rollback | `503` |
| `42` | Syntax error or access rule violation | `internal` | fail | `500` |
| `22` | Data exception | `data_integrity` | fail | `422` |
| `53` | Insufficient resources | `resource_exhausted` | degrade | `503` |

## Cheat sheet — scoring scales

| Factor | 1 | 3 | 5 | 8 | 10 |
| ------ | - | - | - | - | -- |
| Severity | cosmetic | confusing message | degraded feature | money or data lost | security breach |
| Occurrence | never seen | yearly | weekly | daily | every call |
| Detection | caught by a test | found in review | found by a metric | rarely noticed | found in production |

- **Risk = severity × likelihood**, both on a 1–5 scale → **1..25**.
- **RPN = severity × occurrence × detection**, each 1–10 → **1..1000**.
- Unmeasured occurrence scores **5**, not 1. Silent modes score detection **10**.

## Decision table — risk → action

| Risk | Action |
| ---- | ------ |
| 15–25 | Fix in the current sprint; add a regression test |
| 8–14 | Schedule; add evidence in the meantime |
| 1–7 | Accept and monitor, or document as a known limitation |

| RPN | Action |
| --- | ------ |
| ≥ 400 | **Blocks the release.** Fix before shipping the change that touches this path |
| 200–399 | Needs a named owner and a dated mitigation plan |
| 100–199 | Backlog; revisit next quarter |
| < 100 | Accept, monitor, document |

## Cheat sheet — the failure-mode inventory row

```yaml
- id: FM-004
  flow: checkout
  point: FP-04                       # chargeStripe
  mode: success_but_response_lost
  category: external_api_ambiguous
  recovery: resolve_later
  severity: 9
  occurrence: 4
  detection: 8
  rpn: 288
  risk: 16
  owner: payments
  status: open                       # open | mitigated | accepted | retired
  mitigation: resolve by charge id before retrying
  regression_test: checkout/ambiguous-charge.spec.ts
  last_reviewed: 2026-04-02
```

**Required fields:** id · flow · point · mode · category · recovery · severity · occurrence ·
detection · rpn · risk · owner · status · last_reviewed.

## Cheat sheet — limits and budgets

| Limit | Value |
| ----- | ----- |
| Failure points per request flow | 8–15 |
| Failure points per background job | 10–20 |
| Guide words per point | 12 |
| Raw modes before pruning | ~12 × points (≈ 144 for 12 points) |
| Rows after pruning | 20–40 (a 50–70% reduction) |
| `maxAttempts` per policy | ≤ 5 |
| `total_deadline_ms` per policy | ≤ 30000 |
| Retry budget | ≤ 10% of the request deadline |
| Dependency timeout | < the caller's remaining budget |
| Enumeration time | ~30 min per flow (first pass), ~10 min after |

## Cheat sheet — SLO and error budget

| SLO | Error budget per month (30.4 days) | Effect on a gap |
| --- | ---------------------------------- | ----------------- |
| 99.9% | 43 m 49 s | one gap at 0.4% of traffic can eat 40% of it |
| 99.99% | 4 m 23 s | every retry policy needs its own budget line |

## Cheat sheet — the boundary checklist

```text
- timeout shorter than the caller's remaining budget
- 200 with a bad body is a mode, not a success
- a lost response is ambiguous, never transient
- circuit breaker or budget, not just a timeout
- every retry at the boundary carries an idempotency key
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Failure point** | A place where control can leave the happy path |
| **Failure mode** | The specific way a failure point fails |
| **Guide word** | A prompt that generates modes mechanically |
| **Category** | The routing key that selects a recovery policy |
| **Policy** | What the system does: fail, retry, compensate, degrade, terminate, resolve later |
| **Ambiguous outcome** | The effect may or may not have happened |
| **Totality** | Every mode maps to a category; every category maps to a policy |
| **Unhandled cell** | A mode with no category, or a category with no policy — the deliverable |
| **Linearization point** | The step after which the effect is committed |
| **Compensation** | The undo of an effect that already happened |
| **Blast radius** | How many customers and how much data a mode affects |
| **Risk** | severity × likelihood, on a 1–5 scale each (1..25) |
| **RPN** | severity × occurrence × detection, 1–10 each (1..1000) |
| **Failure-mode inventory** | The durable, scored, owned list of modes in the repository |

## Related

- [Chapter 52 — Failure-Path Analysis](../README.md)
- [Failure-Path Analysis of the Checkout Flow](../03-practical-examples/01-checkout-failure-path-analysis.md)
- [FMEA, the Failure-Mode Inventory, and Risk Prioritization](../02-deep-dive/01-fmea-and-risk-prioritization.md)
- [Chapter 51 — Reference](../../51-correctness-properties-of-error-handling/05-reference/README.md)
