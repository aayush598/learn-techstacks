# Chapter 51 — Reference

> Part XX · Chapter 51 · The 18-property checklist, verification matrix, and glossary.

## The 18 correctness properties — sign-off checklist

Print this. One line per property, filled in with the evidence you can point at.

| # | Property | Definition | Evidence to attach | ✅/❌ |
| - | -------- | ---------- | ------------------ | ----- |
| 51.1 | Defined outcome per failure path | Every failure path reaches one declared terminal state | Outcome enum + `assertNever` + terminal-row query | ☐ |
| 51.2 | Never silently discarded | Every caught error propagates, translates, or is recorded | Error-count vs terminal-record reconciliation = 0 | ☐ |
| 51.3 | Deterministic classification | Same error ⇒ same code, category, retryability | Golden-corpus test over the classifier | ☐ |
| 51.4 | Causes recoverable | The original cause and vendor context survive | Error object shows `cause`, vendor code, request ID, attempt | ☐ |
| 51.5 | No sensitive exposure | Outbound errors are projections through an allowlist | Canary-secret test on all three channels | ☐ |
| 51.6 | Retries terminate | Bounded attempts, elapsed deadline, and budget | Policy constants + retry-budget metric | ☐ |
| 51.7 | Cleanup occurs | Resources released on success, failure, timeout, cancellation | Pool/transaction/timer counters return to zero | ☐ |
| 51.8 | Consistency preserved | Invariants hold in every observable state, including post-failure | Invariant query after every failure scenario | ☐ |
| 51.9 | No duplicate side effects | N deliveries ⇒ at most one observable effect | Unique constraint + effect-count assertion | ☐ |
| 51.10 | Responses follow contracts | Every emitted error matches the published shape and status | Schema validation over all error paths | ☐ |
| 51.11 | Safe fallback for unknown | The default branch fails safe, never to success | Reviewed default policy row + default-branch test | ☐ |
| 51.12 | No unbounded recursion | Retry, fallback, translation, and cause chains are bounded and acyclic | Depth counters asserted below the caps | ☐ |
| 51.13 | Concurrency-safe | N concurrent duplicates ⇒ at most one effect | Concurrent-delivery test (N = 10–50) | ☐ |
| 51.14 | Partial failures accurate | successes + failures == attempted, per item | Batch result invariant assertion | ☐ |
| 51.15 | Cancellation not success | A cancelled operation never reports success | Cancellation test + `cancelled` state | ☐ |
| 51.16 | Recovery preconditions | Recovery runs only when its preconditions hold | `decideRecovery()` + stop-reason records | ☐ |
| 51.17 | Transformations preserve metadata | Translation keeps code, category, retryability, cause, context | Field-by-field translation property test | ☐ |
| 51.18 | Predictable during dependency failures | Behaviour is a function of dependency state | Dependency-outage drill with a stated outcome | ☐ |

## Property → verification technique

| Property | Test | Invariant query | Structural mechanism | Review |
| -------- | ---- | -------------- | -------------------- | ------ |
| 51.1 | Outcome enum exhaustiveness | No rows in a non-terminal state > 15 min | Closed union + `assertNever` | Read the catch list |
| 51.2 | No-discard lint rule | Unmatched error events = 0 | Mandatory disposition in the catch template | "Where does this go?" |
| 51.3 | Golden-corpus test | n/a | Single pure `classify()` | One classifier? |
| 51.4 | Cause-presence assertion | n/a | Required `cause` in the constructor | Error payload review |
| 51.5 | Canary-secret test | Secret scan on error output | Public DTO projection | Payload diff |
| 51.6 | Attempt/depth counters | Retry rate ≤ 10% of traffic | Bounded retry helper | Constants review |
| 51.7 | `afterEach` invariant | Pool checked-out = 0 | Scope-managed resources | Resource scope review |
| 51.8 | Post-failure scenario test | Invariant SQL after each scenario | State machine in the schema | State diagram review |
| 51.9 | Duplicate-delivery test | Duplicate effects = 0 | Unique constraint + idempotency key | Dedupe design review |
| 51.10 | Contract test over all paths | n/a | One response builder + schema | Body diff review |
| 51.11 | Default-branch test | Unknown errors = 0 in normal operation | Total policy table | Default row review |
| 51.12 | Depth counter assertion | n/a | Depth caps in helper signatures | Chain inspection |
| 51.13 | Concurrent-delivery test | Duplicate effects = 0 | Atomic DB operations | Shared-state scan |
| 51.14 | Batch invariant assertion | successes + failures == attempted | Batch result type | Report shape review |
| 51.15 | Cancellation test | No `success` rows for aborted ops | `cancelled` in the outcome union | Abort-handling review |
| 51.16 | Stop-reason assertion | Recovery stops logged with reasons | `decideRecovery()` | Precondition table review |
| 51.17 | Translation field test | n/a | Translation table with explicit fields | Wrapper review |
| 51.18 | Dependency-outage drill | Latency p99 during the outage | Per-dependency policy object | Policy coverage review |

## Key limits and defaults

| Limit | Value | Applies to |
| ----- | ----- | ----------- |
| Retry attempts | 3–5 | Remote calls |
| Retry base delay | 200 ms–1 s, exponential, full jitter | Remote calls |
| Retry cap | 30 s | Retry delay |
| Retry total deadline | < caller deadline (e.g. 8 s of 30 s) | Remote calls |
| Retry budget | ≤ 10% of request volume | All retries |
| Cleanup timeout | ~2 s | Resource release |
| Fallback chain depth | ≤ 3 | Dependency fallbacks |
| Translation depth | ≤ 5 | Error translation |
| Cause chain depth | ≤ 10 | Error nesting |
| Concurrent-duplicate test size | 10 (50 for money) | Property tests |
| Public error fields | 4–6 | Error responses |
| Retry window (payments) | 24 h | Idempotency records |
| Dedupe window (webhooks) | 30 d | Event dedupe records |
| Webhook signature tolerance | 300 s | Signature validation |
| SLO 99.9% budget | 43.2 min / 30 days | Availability |
| SLO 99.95% budget | 21.6 min / 30 days | Availability (financial paths) |

## Risk and prioritization

```text
   risk = severity (1–5) × likelihood (1–5)      → 1..25
   RPN  = severity × occurrence × detection (1–10 each)  → 1..1000
```

| Risk | Action |
| ---- | ------ |
| 15–25 | Fix in the current sprint; add a regression test |
| 8–14 | Schedule; add evidence in the meantime |
| 1–7 | Accept and monitor, or document as a known limitation |

Recommendation: treat **RPN ≥ 200** as "needs an action" and **RPN ≥ 400** as "blocks release".

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Correctness property | A falsifiable claim about all failure paths |
| Terminal outcome | A state from which no further progress happens |
| Silent discard | A caught error that is neither propagated nor recorded |
| Classification | The mapping from a raw error to code, category, and retryability |
| Linearization point | The single step after which an effect is committed |
| Recovery precondition | A condition that must hold before a recovery action is taken |
| Stop reason | The recorded explanation for declining to recover |
| Dedupe window | The period during which a duplicate operation is detected and ignored |
| Fault mode | The shape of an injected failure (throw, delay, crash, partial, duplicate, wrong data) |
| Oracle | The assertion that tells you a property held |

## Signposts

- Finding the failure paths → [Ch. 52 Failure-Path Analysis](../../52-failure-path-analysis/README.md)
- Retry and idempotency mechanics → [Ch. 27](../../../part-11-retry-and-resilience/27-retry-policies/README.md) · [Ch. 28](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- Translation details → [Ch. 16](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- Leakage controls → [Ch. 34](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)

## Related

- [Chapter 51 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 51 index](../README.md)
- [Part XX index](../../README.md)
