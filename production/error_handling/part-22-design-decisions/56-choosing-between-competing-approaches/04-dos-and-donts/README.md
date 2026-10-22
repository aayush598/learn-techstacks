# Chapter 56 — Do / Don't

> Part XXII · Chapter 56 · all sections · _Estimated reading time: 8 min_

The consolidated rules for choosing between competing error-handling approaches. Use the
tables as a PR checklist; the review questions at the bottom are the ones worth arguing
about.

## Control-flow shape rules (56.1, 56.7, 56.14)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return a result when the caller can enumerate the failure set (56.1) | Throw for expected business outcomes |
| Pick one shape **per layer** and write the rule down (56.7) | Mix exception and result styles with no boundary |
| Aggregate **independent** failures (56.14) | Aggregate failures that are ordered and dependent |
| Cap collected failures and report truncation | Collect unbounded failures into memory |
| Use `422` for aggregated field validation | Use `400` or `500` for invalid input |
| Treat a duplicate webhook as a success | Return `409` and trigger a retry storm |

## Structure and ownership rules (56.2, 56.3, 56.9–56.12)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize the **decision**; localize the **effect** (56.2) | Centralize business decisions in a global handler |
| Keep one base class with universal fields only (56.3) | Add domain fields to the global error class |
| Express variants as a discriminated union (56.9) | Build a 5-level exception hierarchy |
| Keep hierarchies ≤ 2 levels deep (56.11) | Build a universal tree for the whole company |
| Own codes in the feature that can explain them (56.12) | Put `CHECKOUT_*` in the shared kernel |
| Promote to shared at **3 real consumers** (56.12) | Extract on first use "for consistency" |

## Recovery policy rules (56.4, 56.5, 56.6, 56.15, 56.16)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "**has the effect happened?**" before choosing retry vs compensation (56.6) | Retry because "it might work" |
| Retry only transient + idempotent + within-deadline failures (56.5) | Retry `422` because the client "will fix it" |
| Mark every degraded response with `degraded: true` + a reason (56.4) | Return a plausible-but-wrong value |
| Compensate in **reverse** order of completed steps (56.6) | Compensate in the order the steps ran |
| Make compensations idempotent (56.6) | Assume a compensation ran exactly once |
| Keep user-facing operations synchronous (56.15) | Defer a checkout failure to a background job |
| Terminate on corruption, recover on request failure (56.16) | Continue after an invariant violation |

## Fidelity and risk rules (56.8, 56.13, 56.17, 56.18)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve `cause`, vendor code, and vendor request ID (56.8) | Rebuild the vendor code from the message |
| Wrap only to add domain meaning (56.8) | Wrap at every layer for readability |
| Validate strictly at untrusted boundaries (56.13) | Coerce money and IDs with `Number()` |
| Ignore unknown vendor fields but record their names (56.13) | Reject a Stripe event because it gained a field |
| Give every code and operation a risk tier (56.18) | Apply one retry policy to all errors |
| Derive retry/fallback/alert rules from the tier (56.18) | Hand-write `attempts: 5` at call sites |
| Gate abstractions on the four questions (56.17) | Abstract because the idea "sounds reusable" |

## Review questions worth arguing about

1. **Shape.** For this new function: can the caller enumerate the failures? If yes, why is it
   throwing?
2. **Owner.** Which module owns the *decision* for this error, and which owns the *fallback*?
   If they are the same module, is that deliberate?
3. **Tier.** What is the risk tier of the operation, and which tier did the code implement?
   A mismatch is the finding.
4. **Effect.** If this call fails, has the side effect already happened? Where is that written
   down?
5. **Fidelity.** If this call fails at 3 a.m., which vendor request ID lets support find it?
6. **Indirection.** Does the new layer remove a decision, or only add a name? How many real
   consumers does it have?

## Escalation criteria

Stop the PR and redesign when you see any of:

- A new error class with more than 8 optional fields.
- A `catch` block that returns `null`, `undefined`, or `false` without a durable record.
- A retry loop over a non-idempotent write with no idempotency key.
- A degradation path with no `degraded` marker.
- A shared error package with a product code in it.
- A new shared abstraction with fewer than 3 real consumers.
- A compensation that is not idempotent.
- A retry count written inline at a call site rather than derived from a policy.

## Related

- [Chapter 56 README](../README.md)
- [Reference: Decision Matrices](../05-reference/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../57-error-handling-under-load-and-at-scale/README.md)
