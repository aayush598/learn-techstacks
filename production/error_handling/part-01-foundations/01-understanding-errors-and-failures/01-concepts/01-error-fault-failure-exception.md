# Error, Fault, Failure, and Exception

> Part I · Chapter 1 · Sections 1.1–1.3 · _Estimated reading time: 15 min_

## In one sentence

A **fault** is the defect, an **error** is the incorrect state it produces, and a **failure** is
when that state becomes externally observable — while an **exception** is merely the language
mechanism used to signal the error.

## Why this matters in production

When a team treats these words as synonyms, three specific bugs appear:

- **Faults are "handled" instead of prevented.** The bug (a null dereference) is wrapped in a
  `try/catch` that logs and continues, so the root cause is never fixed.
- **Failures are contained too late.** The error is allowed to reach the API boundary before
  anyone asks "should this have failed fast?"
- **Recoverable errors are escalated as failures.** A transient deadlock triggers a 500 to the
  user instead of an invisible retry.

The cost is measurable: retried invalid writes, user-visible outages from avoidable propagation,
and alert fatigue.

## The causal chain

```text
  FAULT (defect)            ERROR (state)               FAILURE (effect)
  ┌──────────────┐          ┌──────────────┐            ┌──────────────┐
  │ code bug     │  causes  │ wrong value  │  becomes   │ wrong result │
  │ misconfig    │ ───────▶ │ bad state    │ ─────────▶ │ visible to a │
  │ env mismatch │          │ in memory/db │            │ user/system  │
  └──────────────┘          └──────────────┘            └──────────────┘
        ▲                          ▲                          ▲
     fix here                 detect here               contain here
   (prevention)              (validation, checks)      (boundaries, retries)
```

- **Fault** — the *static* cause: a bug, a typo in a config, a wrong assumption about an SDK.
  Faults are often dormant; they only manifest under specific conditions.
- **Error** — the *dynamic*, internal deviation: a variable holds `null`, a total is negative, a
  connection object is dead. Errors may be detected (assertions, validation) or may silently sit.
- **Failure** — the *externally visible* deviation: the API returns 500, the invoice is wrong, the
  page spins forever. A failure is an error that crossed the system boundary.
- **Exception** — a *mechanism*, not a thing to fix. Rust's `Result`, Go's `error` value, JS's
  `throw`, and Java's checked exceptions are all ways to signal an error; none of them is the
  error itself.

## Definitions (use these exactly)

| Term | Definition | Where you act on it |
| ---- | ---------- | ------------------- |
| **Fault** | The defect or misconfiguration that can produce an error. | Prevention: review, tests, config validation |
| **Error** | The discrepancy between the current state and the specified (correct) state. | Detection: assertions, invariants, validation |
| **Failure** | The event where the delivered behavior deviates from the specification as observed by an external party. | Containment: boundaries, fallbacks, API contracts |
| **Exception** | A control-flow mechanism for signaling an error. | Propagation: try/catch, `Result`, error returns |

## Why the distinction changes your code

Consider a payment capture that reads `amount` as a string, parses it, and charges a card.

```ts
// The FAULT is the assumption that amount is always numeric.
// The ERROR is `NaN` produced by Number("abc").
// The FAILURE is a user charged the wrong (or zero) amount.
function charge(amountInput: string) {
  const amount = Number(amountInput); // error created here silently
  return gateway.charge({ amount });  // failure realized here
}
```

Three different fixes target three different stages:

1. **Prevent the fault** — validate the DTO at the trust boundary so `amountInput` is typed as a
   validated `Money`, not `string`.
2. **Detect the error** — assert `Number.isFinite(amount)` and reject `NaN` immediately.
3. **Contain the failure** — if a `NaN` somehow reaches the gateway, fail with a *validation*
   response, not a charge, and never let it become a 200.

> ⚠️ **Hazard.** The most dangerous pattern is when an error is *not* allowed to become a failure
> where it should (silent wrong result), or when it *becomes* a failure where it should have been
> recovered (a transient blip surfaced to the user).

## Exceptions are not errors

An exception carries an error, but not every error is an exception and not every exception is an
error:

- A `404 Not Found` is an *expected outcome*, commonly implemented without throwing.
- A `CancellationException` is a *control signal*, not a defect.
- A `Result.Err(ValidationFailed)` in Rust is an error represented as a value.

Treating "exception" and "error" as synonyms leads teams to encode business decisions as throws
and lose them in global handlers.

## Real-world use case — Acme SaaS

Acme's `ExportJob` writes rows to an S3 object. A faulty retry loop creates an **error**: it
appends duplicate rows because it re-reads a stale offset. The **failure** is a customer's CSV
containing 2× its expected rows, discovered during an audit. Root cause: no idempotent write key.
The fix targets the fault (add a deterministic object key), not the symptom.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Say "this is a transient error, retry" or "this is a fault, fix it" | Use "error" for all four concepts |
| Fix faults; detect errors; contain failures | `catch` a fault and continue silently |
| Use exceptions as one mechanism among several | Equate "exception" with "error condition" |

## Common mistakes

- **Wrapping the fault instead of fixing it.** A catch-all that logs a null-pointer bug hides it
  forever.
- **Using "failure" for something internal.** If no external observer can see it, it is still an
  error, not (yet) a failure.
- **Confusing exceptions with failures.** An uncaught exception is a mechanism failure; the
  underlying error may be ordinary.

## Checklist

- [ ] Can you label every recent bug as fault / error / failure?
- [ ] Does each error have a detection point, or can it sit silently?
- [ ] Is each failure contained at a boundary you chose deliberately?
- [ ] Do you avoid using "exception" interchangeably with "error"?

## Related

- [The Fifteen Dimensions of Failure](./02-the-fifteen-dimensions.md)
- [Failure Domains and Fault Boundaries](../02-deep-dive/01-failure-domains-and-fault-boundaries.md)
- [Glossary: error, fault, failure, exception](../../../GLOSSARY.md)
