# Chapter 46 — Reference

> Part XVII · Chapter 46 · all sections · _Estimated reading time: 8 min_

Cheat sheets for the pattern catalog: the selection table, the anti-pattern quick reference,
the simplest-pattern rule, the chapter glossary, and signposts into the long-form files.

## 1. Pattern-selection decision table

| If the requirement is… | Use | Not | Key data |
| ---------------------- | ---- | --- | -------- |
| Every error has exactly one defined external exit | Global handler (46.1) | Per-route catch-alls | 1 per transport |
| A vendor's error shape must not leak past one file | Error adapter (46.2) | `instanceof` checks in services | 1 function per vendor |
| A failure is expected, frequent, and every caller must handle it | Result type (46.3) | Exceptions for in-contract branching | switch above ~1% of calls |
| Clients, docs, and SDKs must agree on status and retryability | Code registry (46.4) | Status literals in controllers | 1 entry per code |
| A foreign error must keep its root cause and its retry semantics | Translation (46.5) | Re-wrapping at every layer | 1 hop per dependency |
| The failure is transient **and** the operation is repeatable | Named retry policy (46.6) | Inline loops; retry-all | 3 attempts (5 for jobs) |
| A dependency outage would exhaust your pool or threads | Circuit breaker (46.7) | One global breaker; no timeout beneath it | 5 failures / 10 s → open 30 s |
| An optional feature has an honest degraded value | Fallback (46.8) | Unwritten fallbacks; fallback on writes | 1 level, documented |
| One failing feature must not fail the page, job, or request | Error boundary (46.9) | A boundary at every call | ~14 boundaries / 40 endpoints |
| A multi-step flow across stores already committed steps | Compensation (46.10) | A transaction rollback | Reverse order; committed steps only |
| Invalid state would compound if the flow continued | Fail-fast (46.11) | Late validation | Earliest detectable point |
| The decision affects money, data integrity, or access | Fail-safe (46.12) | Default-allow; default-retry | Unknown authz → deny |
| None of the above is true yet | **Simplest pattern (46.26)** | A resilience stack | 3 files: error, call site, handler |

## 2. The six-question flowchart

```text
1. Is the failure expected & frequent in this function? ── yes ─▶ Result type (46.3)
2. Is the operation non-idempotent and the failure ambiguous? ── yes ─▶ NO retry;
        surface AMBIGUOUS_OUTCOME + reconcile (46.24)
3. Is the failure classified transient & safe to repeat? ── yes ─▶ named retry (46.6)
4. Is this a later step of a multi-step workflow? ── yes ─▶ compensate prior steps (46.10)
5. Does the feature have an honest degraded value? ── yes ─▶ boundary + fallback (46.9 / 46.8)
6. Otherwise ──▶ typed error, throw, boundary owns the exit (46.26 + 46.1)
```

**Composition order that avoids amplification:** `boundary → breaker → retry → adapter → vendor`.
Translation sits innermost; serialization only at the boundary; the status decision exists once,
in the registry.

## 3. Anti-pattern quick reference

| ID | Name | One-line tell | Cheapest fix |
| -- | ---- | ------------- | ------------ |
| 46.13 | Catch-all | One generic `500` for every failure | Delete the local catch |
| 46.14 | Empty catch | `catch (e) {}` | Log at debug with a stated degradation, or rethrow |
| 46.15 | Swallow-and-continue | The flow continued after a required side effect failed | Make the side effect part of the unit of work (or an outbox) |
| 46.16 | Exception-driven business flow | "Not found" thrown and caught three layers up | Return `Result` / `null` |
| 46.17 | Excessive custom classes | 40+ classes that differ only in name | Collapse to behavior classes; specifics in `code` |
| 46.18 | Generic messages | "An error occurred" / `ERR_1001` | Message = condition + salient values; code = routing |
| 46.19 | Deep wrappers | `ErrorWrapper(…(…(original)))` | Wrap only where the type changes; rethrow otherwise |
| 46.20 | Repeated retry logic | Two `attempts` constants for one dependency | One shared module, named policies |
| 46.21 | Catch-log-without-rethrow | The catch block's only statement is a log call | Rethrow, recover, or declare optional — pick one |
| 46.22 | Success-shaped failure | `200` + `{"success": false}` | Non-2xx status from the registry |
| 46.23 | Treat all as retryable | The same predicate for declines and timeouts | `retryOn: (e) => e.retryable` |
| 46.24 | Retry non-idempotent | A write path retried with no idempotency key | Key it, or surface `AMBIGUOUS_OUTCOME` and reconcile |
| 46.25 | Overengineering | A framework with one consumer and no incident behind it | Apply 46.26; delete unjustified mechanisms |
| 46.26 | Simplest pattern | Typed error thrown once, caught once at the boundary | **This is the destination, not a shortcut** |

**Severity:** 46.24 and 46.15 first (money and data), then 46.22 and 46.21 (hidden outages),
then 46.13 and 46.19 (debuggability), then 46.17 and 46.25 (reader tax).

## 4. The "simplest pattern that satisfies the requirement" rule

**The rule:** the simplest pattern that satisfies the requirement wins. A typed error thrown in
the layer that detects it and caught once at the boundary that owns the fallback is
**production-grade**, not a shortcut. Every additional mechanism must beat it with a number.

**The three-file baseline (46.26):**

```text
features/<feature>/errors.ts   → the typed error + its registry code
features/<feature>/<svc>.ts    → throw site (no framework visible)
transports/http/error-handler.ts → the one place that maps code → status
```

**Escalation test — add a mechanism only when all three are true:**

1. There is a **named incident or metric** (a 40-minute Stripe outage that exhausted the pool).
2. The simpler pattern provably fails for a **stated reason** ("the boundary returns 500 but
   the request should succeed after a transient blip").
3. The mechanism has a **named owner and a written policy** (numbers in
   `shared/resilience/retry-policies.ts`, not at the call site).

**Kill criteria:** a mechanism with one consumer and no incident after two quarters is deleted,
unless deleting it would break a runbook written from a real event.

**A worked judgement at Acme:** `AgentRun` shipped with a retry wrapper, a provider breaker, and
a three-step fallback chain. Six weeks of measurements: the breaker never opened, the fallback
fired twice, and the nested retry inside the provider SDK produced double retries on rate
limits. Meanwhile `ExportJob` — on the simple pattern alone — had better incident metrics. The
corrective action was **subtractive**: keep the adapter translation and the named retry policy,
drop the unused breaker and one fallback layer. Framework lines of code: −60%, no user-visible
regression.

## 5. Numbers worth memorizing

| Fact | Value |
| ---- | ----- |
| Global handlers | 1 per transport (HTTP, job runner, `WebhookIngest`, CLI) |
| Adapters | 1 translation function per vendor SDK |
| Registry entries at Acme | 45 codes, CI rejects a code with no entry |
| Result-type switch threshold | expected failure above ~1% of calls |
| Retry attempts | 3 (sync) / 5 (jobs); full jitter; multiplier 2–4; `Retry-After` wins |
| Retry budget | retries ≤ ~10% of primary traffic per dependency per hour |
| Breaker defaults | 5 failures / 10 s window → open; 30 s open → half-open; 2 successes → closed |
| Boundaries at Acme | ~14 for ~40 endpoints |
| Attempt budget per Checkout capture | ≤ 3 Stripe calls (worst case, breaker open = fast-fail) |
| Un-nested vs nested calls | 3 vs up to 12 provider calls per logical operation |
| Error classes (behavior-distinct) | ~15–30 for a mid-size SaaS; Acme collapsed 61 → 14 |
| Error class count as a smell | > 1 class per distinct category + retryable + handling combo |
| `WebhookIngest` ack policy | bad signature → `400` (stop retrying); transient → `503` + backoff |

## 6. Stable status mapping used by the registry

| Category | Code example | HTTP | Retryable |
| -------- | ------------ | ---- | --------- |
| Payment declined | `CHECKOUT_CARD_DECLINED` | 402 | ❌ |
| Not found | `PROJECT_NOT_FOUND` | 404 | ❌ |
| Conflict | `PROJECT_SLUG_TAKEN` (Postgres `23505`) | 409 | ❌ |
| Validation | `EXPORT_PARSE_MALFORMED_CSV` | 422 | ❌ |
| Rate limited | `DEP_STRIPE_RATE_LIMITED` (vendor `429`) | 429 | ✅ after `Retry-After` |
| Dependency down | `DEP_STRIPE_UNAVAILABLE` | 503 | ✅ |
| Dependency timeout | `DEP_LLM_TIMEOUT` | 504 | ⚠️ only if idempotent |
| Ambiguous outcome | `PAYMENT_AMBIGUOUS_OUTCOME` | 503 | ❌ (reconcile instead) |
| Compensation failed | `COMPENSATION_FAILED` | 500 | ❌ (page a human) |
| Unexpected | `INTERNAL_UNEXPECTED` | 500 | ❌ |

## 7. Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Global handler** | The one catch-all per transport that owns the final external outcome |
| **Error adapter** | The single translation function for one vendor SDK |
| **Error boundary** | A line where the fallback differs from propagation, so the error is contained there |
| **Code registry** | Pure data mapping each code to its status, retryability, and public title |
| **Translation** | Converting a foreign error into the app model once, preserving `cause` |
| **Named retry policy** | A shared, referenced policy — not a loop written at the call site |
| **Circuit breaker** | Closed/open/half-open state machine that stops calling a failing dependency |
| **Fallback** | A defined substitute value for a failed primary path |
| **Compensation** | A business-level undo of a step that already completed |
| **Fail-fast** | Abort at the earliest detectable invalid state |
| **Fail-safe** | Choose the safe state under uncertainty, even at the cost of availability |
| **Simplest pattern (46.26)** | Typed error thrown once, caught once at the boundary — the default |
| **Behavior class** | One error type per distinct category + retryable + handling combination |
| **Ambiguous outcome** | A call whose success cannot be determined (timeout after send) |
| **Documented-optional** | A catch that is explicitly allowed to degrade, with the degradation written down |
| **Compounding chain** | A sequence of anti-patterns where each one enables the next (Chains A–E) |
| **Rule of three** | Build the shared abstraction on the third concrete use, not the first |

## 8. Signposts

- Global handler, adapter, boundary, compensation → [Structural Patterns](../01-concepts/01-structural-patterns.md)
- Result type, registry, translation → [Modeling Patterns](../01-concepts/02-modeling-patterns.md)
- Retry, breaker, fallback, fail-fast, fail-safe, simplest pattern → [Resilience and Control-Flow Patterns](../01-concepts/03-resilience-and-control-flow-patterns.md)
- Catch-all, empty catch, swallow, generic messages, wrappers, success-shaped failures → [Handling Anti-Patterns](../01-concepts/04-handling-anti-patterns.md)
- Class sprawl, repeated retries, retry-all, non-idempotent retry, overengineering → [Design Anti-Patterns](../01-concepts/05-design-anti-patterns.md)
- Result vs exception, global vs local, retry vs compensate → [Pattern Selection Trade-Offs](../02-deep-dive/01-pattern-selection-trade-offs.md)
- Chain remediation order (contract → classification → amplification → structure) → [Anti-Pattern Compounding and Remediation](../02-deep-dive/02-anti-pattern-compounding-and-remediation.md)
- Before/after diffs for the six refactor families → [Before/After Anti-Pattern Refactors](../03-practical-examples/02-before-after-anti-pattern-refactors.md)
- Where the code lives → [Chapter 45 — Organizing Error-Handling Modules](../../45-organizing-error-handling-modules/README.md)
- Retry depth → [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- Saga semantics → [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- HTTP status selection → [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)

## Related

- [Chapter 46 Do / Don't](../04-dos-and-donts/README.md)
- [Chapter 46 README](../README.md)
- [Part XVII Index](../../README.md)
- [Glossary](../../../GLOSSARY.md)
