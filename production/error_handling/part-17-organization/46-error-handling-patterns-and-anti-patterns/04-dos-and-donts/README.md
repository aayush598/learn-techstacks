# Chapter 46 — Do / Don't

> Part XVII · Chapter 46 · all sections · _Estimated reading time: 9 min_

The reviewable ruleset for the pattern and anti-pattern catalog. Every table is written to be
pasted into a PR template or a design-review doc: one rule per row, and a rule that cannot be
checked from the diff is not a rule. The examples are Acme SaaS's own: the Checkout capture,
the `ExportJob` worker, the `WebhookIngest` transport, and the optional `AgentRun` summary.

## Global handler (46.1)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep **exactly one** global handler per transport (HTTP, job runner, `WebhookIngest`, CLI) | Add a second catch-all "for safety" inside a controller |
| Read `code` / `category` / registry metadata and emit the contract | Branch on `code.startsWith("CHECKOUT_")` to pick a status |
| Log once, with the correlation id, and never echo stacks or vendor payloads | Log the raw vendor payload to "be helpful" |
| Treat it as the last-resort exit, not the place where errors are handled | Let it recover by returning `200` with an empty body |

## Error adapter (46.2)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Expose **one** `from<Vendor>Error(err)` per vendor SDK | Import a vendor SDK anywhere except its adapter folder |
| Translate only: map shape → app error, keep the original as `cause` | Retry, serialize, or decide a business outcome inside the adapter |
| Preserve `retryable` and permanence (rate limit ≠ timeout ≠ 404) | Map every upstream failure to one generic `DEPENDENCY_ERROR` |
| Default unknown vendor errors to **non-retryable** | Default unknown errors to retryable "to be safe" |

## Result type (46.3)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `Result` where failure is **expected and frequent** (> ~1% of calls) | Use `Result` for genuinely exceptional paths |
| Use a discriminated union so the compiler forces the branch | A loose `E` that erases the guarantee the type promised |
| Pick result-vs-exception **per layer** and write the convention down | Mix throwing and returning `Result` inside one module |
| Use collect-all semantics for batches (`ExportJob` rows) | Abort a 50,000-row import because row 1 was malformed |

## Code registry (46.4)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the registry **pure data**: `httpStatus`, `retryable`, `publicTitle` | Put functions, vendor imports, or message formatting in the registry |
| Have exactly one entry per public code, enforced in CI | Duplicate the code list in a second file "for the docs" |
| Generate the docs page and SDK types from the registry | Hand-maintain a parallel error table |
| Let the transport read the status from the registry | Hardcode `402` in a controller |

## Translation (46.5)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate **once**, where the shape actually changes | Translate again in the controller, the worker, and the serializer |
| Keep the original error reachable as `cause` | Drop the cause to keep the payload "small" |
| Keep the direction foreign → domain | Translate domain errors back into vendor shapes |
| Cap the `cause` chain at one hop per dependency | Wrap at every call-stack frame (46.19) |

## Retry policy (46.6)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reference a **named** policy: `withRetry("stripeHttp", …)` | Inline `attempts: 5` at a call site (46.20) |
| Keep the Checkout capture at ≤ 3 Stripe calls per logical operation | Let a caller loop nest inside the adapter's loop (3 × 5 = 15) |
| Gate `retryOn` on `e.retryable` **and** on idempotency | Retry on any `catch` (46.23) |
| Use exponential backoff with **full jitter**, and honor `Retry-After` | Sleep a fixed 1 s between attempts |
| Own the loop in exactly **one** layer (adapters translate only) | Let the adapter *and* the caller each retry the same call |
| Preserve the final failure when attempts are exhausted | Throw a generic `new Error("failed")` after the loop |

## Circuit breaker (46.7)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each critical dependency its own breaker | Wrap the whole application in one global breaker |
| Put a per-call timeout **underneath** the breaker | Count hangs as failures with no timeout configured |
| Open on dependency failures only — not on a `402` card decline | Count business rejections as breaker failures |
| Start from 5 failures / 10 s window, 30 s open, 2 trial successes | Tune thresholds to taste with no incident data |

## Fallback (46.8)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write the degraded value down **before** shipping the fallback | Fall back to a value nobody agreed on |
| Say out loud when data is stale or partial | Serve a stale Checkout total as if it were current |
| Bound the fallback chain (one level) | Cascade through three fallbacks, each calling the next |
| Never fall back on a required write | Queue a payment "for later" and return success |

## Error boundary (46.9)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Draw a boundary where the fallback **differs** from propagation | Wrap every call in `try/catch` |
| Give each boundary a documented outcome (degrade, partial, translate, rethrow) | Catch and rethrow the same error at each layer (46.19) |
| Keep request, job, and feature boundaries separate | Use one boundary for the whole `ExportJob` worker |
| Let the optional `AgentRun` summary fail without failing the page | Fail the page because an optional widget threw |

## Compensation (46.10)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register a compensation **only for steps that confirmed completion** | Compensate a Checkout charge that never committed |
| Run compensations in **reverse** order of the committed steps | Run them in forward order |
| Treat a failed compensation as an incident (`COMPENSATION_FAILED`) | Swallow a failed refund and continue |
| Use compensation for cross-store flows only | Compensate inside a single Postgres transaction |

## Fail-fast (46.11)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Abort at the **earliest** point the invalid state is detectable | Push a bad record to the end of the pipeline and hope |
| Guard preconditions at service entry (tenant suspended, plan inactive) | Charge a card for a suspended tenant and refund later |
| Fail fast on internal invariants with an `assert` | Continue with a half-initialized object |
| Map the fast failure to a clean 4xx at the boundary | Let a fail-fast internal error become a 500 with a stack trace |

## Fail-safe (46.12)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| **Deny** when an authorization result is unknown | Default-allow when the policy service is unreachable |
| Treat an unknown error classification as non-retryable | Default-retry unknown failures "to be safe" |
| Do not auto-retry an ambiguous commit without an idempotency key | Retry a payment whose outcome you do not know |
| Record explicit fail-open choices (e.g. the recommendation widget) | Let fail-open happen by accident |

## The simplest pattern (46.26)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Default to a typed error thrown in the detecting layer, caught once at the boundary | Start a feature with a retry stack, a breaker, and a saga |
| Require a **measured** justification for every added mechanism | Add resilience machinery because another repo has it |
| Abstract on the third concrete use (rule of three) | Abstract on the first use "for consistency" |
| Delete mechanisms with no incident and no consumer after two quarters | Keep "unused" fallbacks alive out of fear |

## Anti-pattern catalog (46.13–46.26)

Severity order: **46.24 and 46.15 corrupt money and data; 46.22 and 46.21 hide outages; 46.13
and 46.19 destroy debuggability; 46.17 and 46.25 tax every future reader; 46.14 and 46.16 are
sloppiness that spreads.**

| ID | Anti-pattern | Symptom (what you see) | Root cause | Fix |
| -- | ------------ | ----------------------- | ---------- | --- |
| 46.13 | Catch-all | Every failure is a generic `500`; clients cannot branch | A blanket `catch` at the wrong layer | Delete the local catch; let the global handler read registry metadata |
| 46.14 | Empty catch | The failure exists nowhere — no log, no metric | Silence to satisfy the compiler | Log at debug with a stated degradation, or rethrow |
| 46.15 | Swallow-and-continue | The workflow "succeeded" but a required side effect is missing | Optional and required work treated identically | Include the side effect in the unit of work, or use an outbox |
| 46.16 | Exception-driven business flow | "Not found" thrown and caught across three layers | Exceptions used for in-contract branching | Return `Result` / `null` for expected absence |
| 46.17 | Excessive custom classes | 40+ classes, all `category: "internal"`, all → 500 | One class per entity or per incident | Collapse to behavior classes; keep specifics in `code` + `details` |
| 46.18 | Generic messages | "An error occurred" with code `ERR_1001` | Messages written to be vague | Message states the condition and salient values; code does the routing |
| 46.19 | Deep wrappers | `ErrorWrapper(…(…(original)))`, five hops deep | Wrapping at every layer | Wrap only where the type changes; otherwise rethrow unchanged |
| 46.20 | Repeated retry logic | Two policies for one dependency; worst case 30 provider calls | Loops written independently per call site | One shared implementation; named policies referenced by name |
| 46.21 | Catch-log-without-rethrow | "We saw it in the logs" — and the flow continued anyway | Logging mistaken for handling | Rethrow, recover, or declare it optional — pick one |
| 46.22 | Success-shaped failure | `200` with `{"success": false}`; the 5xx dashboard is blind | Failure encoded in the response body | Map to a non-2xx status through the registry |
| 46.23 | Treat all as retryable | A declined card retried 5 times; the user waits 30 s | No classification at the catch | `retryOn: (e) => e.retryable`; unknown → non-retryable |
| 46.24 | Retry non-idempotent | One customer charged twice; a 9-day refund | Ambiguous failure plus blind re-execution | Idempotency key, or surface `PAYMENT_AMBIGUOUS_OUTCOME` and reconcile |
| 46.25 | Overengineering | A 1,100-line error framework with one consumer | Generality built before the need existed | Apply 46.26; justify each mechanism with an incident or a number |
| 46.26 | Simplest pattern (**the antidote**) | Typed error thrown once, caught once at the boundary | — | The target state: one code, one registry entry, one defined exit |

## Review questions worth arguing about

1. **Which pattern is this PR adding, and which row justified it?** "It might be useful later"
   is not a row; a named incident or a number is.
2. **Where does this error get caught?** Name the layer. If nobody can, it is a swallowed error
   (46.14 / 46.21).
3. **Is the operation safe to repeat?** If not: where is the idempotency key, or is the
   ambiguous outcome surfaced?
4. **Does the contract lie?** Check that the status is non-2xx and came from the registry.
5. **What is the fallback, in one sentence?** "It logs" is not a fallback.

## Escalation criteria

Stop the PR and redesign when you see any of:

- A second global handler for the same transport.
- A retry loop whose numbers are not in `shared/resilience/retry-policies.ts`.
- A retried write path with no idempotency key and no `AMBIGUOUS` classification.
- A `200` response body containing `success: false` or an `error` field.
- An error class that differs from an existing one only in name.
- A new resilience mechanism with no recorded incident or metric behind it.

## Chapter checklist

- [ ] Exactly one global handler per transport; it makes no business decisions.
- [ ] Each vendor SDK is imported only by its adapter; adapters translate only.
- [ ] The layer convention for result vs exception is written down and followed.
- [ ] Every public code has exactly one registry entry; CI enforces it.
- [ ] Every catch ends in **throw / recover / documented-optional** — never log-only.
- [ ] No response returns a success status with an in-body failure marker.
- [ ] Every retry references a named policy and is gated on `e.retryable`.
- [ ] Every retried write path is keyed or explicitly classified non-retryable.
- [ ] Every breaker sits under a timeout and counts dependency failures only.
- [ ] Every fallback has a written degraded value and a comms plan.
- [ ] Every boundary has a documented outcome; no boundary without a decision.
- [ ] Every saga step has a named compensation with a tested failure path.
- [ ] Unknown classification → non-retryable; unknown authorization → deny.
- [ ] Error class count ≈ behavior-distinct handling, not entity count.
- [ ] Each resilience mechanism has a written justification (incident or number).

## Related

- [Chapter 46 README](../README.md)
- [Reference: Pattern Selection & Anti-Pattern Catalog](../05-reference/README.md)
- [Pattern Selection Trade-Offs](../02-deep-dive/01-pattern-selection-trade-offs.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../45-organizing-error-handling-modules/README.md)
