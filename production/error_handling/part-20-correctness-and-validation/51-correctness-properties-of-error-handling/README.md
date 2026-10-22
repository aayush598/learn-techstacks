# Chapter 51 — Correctness Properties of Error Handling

> Part XX · _Estimated reading time: 110–140 min_
> **Prerequisite:** [Chapter 15 — Error Boundaries](../../part-06-boundaries-and-translation/15-error-boundaries/README.md), [Chapter 16 — Error Translation](../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)

## One-sentence summary

Production error handling is correct when **18 testable statements** hold on every failure path —
and each statement must be backed by evidence you can point a reviewer at.

## Why this chapter matters

Reviewers can tell you that a `catch` block is "handled". They cannot tell you it is *correct*. The
difference shows up months later, in a form nobody can reproduce: a subscription that exists in
the payment provider and nowhere else, an export job that sits in `running` forever, a stack trace
in a customer email, a retry that keeps a queue alive while the database is down.

The industry's answer has been "add more try/catch". That increases the *number* of handled paths
without increasing the number of *defined* paths — and often makes things worse, because a caught
error that is neither propagated nor recorded is a **silent discard**.

This chapter replaces "handled" with **properties**. A property is a claim about all failure paths
that can be true or false, and that can be checked. That framing is what turns error handling from
taste into engineering.

## Chapter map

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-determinism-and-completeness.md`](./01-concepts/01-determinism-and-completeness.md) | 51.1–51.4 | Defined outcomes, no silent discard, deterministic classification, recoverable causes |
| [`01-concepts/02-safety-and-resource-properties.md`](./01-concepts/02-safety-and-resource-properties.md) | 51.5–51.9 | No sensitive exposure, terminating retries, cleanup, consistency, no duplicate effects |
| [`01-concepts/03-transformation-and-contract-properties.md`](./01-concepts/03-transformation-and-contract-properties.md) | 51.10–51.12, 51.17–51.18 | Contract-shaped responses, safe fallback for unknown, bounded recursion, metadata-preserving translation, predictability under dependency failure |
| [`01-concepts/04-concurrency-cancellation-and-partial-properties.md`](./01-concepts/04-concurrency-cancellation-and-partial-properties.md) | 51.13–51.16 | Concurrency safety, accurate partial results, cancellation semantics, recovery preconditions |
| [`02-deep-dive/01-verifying-properties-with-failure-injection.md`](./02-deep-dive/01-verifying-properties-with-failure-injection.md) | 51.1–51.18 | How to produce evidence: fault injection, oracles, property tests |
| [`02-deep-dive/02-enforcing-properties-structurally.md`](./02-deep-dive/02-enforcing-properties-structurally.md) | 51.1–51.18 | Making violations impossible with types, invariants, policy tables, and CI |
| [`03-practical-examples/01-checkout-correctness-audit.md`](./03-practical-examples/01-checkout-correctness-audit.md) | 51.1–51.18 | A full audit of the `Checkout` flow, property by property |
| [`03-practical-examples/02-property-tests-for-webhook-ingest.md`](./03-practical-examples/02-property-tests-for-webhook-ingest.md) | 51.2, 51.9, 51.13, 51.14 | Property-based tests for `WebhookIngest` |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | The 18-property checklist, verification matrix, chapter glossary |

## Learning objectives

By the end you can:

1. State all 18 properties in your own words and give a real violation of each.
2. Decide, for any given error path, whether it satisfies a property — and name the evidence.
3. Design a **property-verification strategy** (fault injection, invariant query, structural
   guarantee) appropriate to the property and the cost of being wrong.
4. Convert a vague "we handle errors" claim into a checklist a reviewer can sign.
5. Detect the four classic violations by reading code: silent discard, unbounded retry, unbounded
   fallback chain, and success-shaped failure.

## The property catalogue

| # | Property | Violation signature | Cheapest evidence |
| - | -------- | ------------------ | ----------------- |
| 51.1 | Defined outcome per failure path | Function can return `undefined`; job stuck `running` | Terminal-state enum + `assertNever` |
| 51.2 | Never silently discarded | `catch {}`, `catch { return null }` | Lint rule + error-count vs terminal-count reconciliation |
| 51.3 | Deterministic classification | Classification by message substring, differs per handler | Golden-corpus test of the classifier |
| 51.4 | Causes recoverable | `new Error("failed")`, dropped `cause` | Cause chain present + vendor code preserved |
| 51.5 | No sensitive exposure | Stack trace, SQL, or PII in the response body | Public DTO projection + canary-secret test |
| 51.6 | Retries terminate | `while (true)` reconnect; nested retries multiply | Ceiling in code + budget metric |
| 51.7 | Cleanup occurs | Resource released only on the success path | Scope guard + leak counter |
| 51.8 | Consistency preserved | Money moved, entitlement missing, no compensation pending | Invariant query run after every failure |
| 51.9 | No duplicate side effects | Duplicate charge / duplicate email on retry | Unique constraint + effect count ≤ 1 |
| 51.10 | Responses follow contracts | `200` with `success: false`; ad-hoc error shapes | Schema validation test on every error path |
| 51.11 | Safe fallback for unknown | Unknown error maps to 200 or to an empty list | Default policy table + audit of the `default` branch |
| 51.12 | No unbounded recursion | Fallback A → B → A; 401 → refresh → 401 → refresh | Depth counter + cycle detection |
| 51.13 | Concurrency-safe | Check-then-act dedupe; double compensation | Concurrent-duplicate test (N=10) |
| 51.14 | Partial failures accurate | "All failed" when 97 of 100 succeeded | successes + failures == attempted |
| 51.15 | Cancellation not success | Cancelled request returns 200 | Terminal state `cancelled` + test |
| 51.16 | Recovery preconditions | Retry after deadline; refund a charge that never happened | Guard function + precondition table |
| 51.17 | Transformations preserve metadata | 429 loses `Retry-After`; 23505 loses constraint name | Translation property test (field-by-field) |
| 51.18 | Predictable during dependency failures | First request hangs 30 s, later ones fail fast | Dependency-failure drill with a stated outcome |

## Key takeaways

1. **A property needs a falsifier.** If you cannot describe how a property would be violated, it is
   a slogan, not a property.
2. **Evidence beats intent.** "We always clean up" is intent; `pool.checkedOut === 0` after 10 000
   failures is evidence.
3. **Some properties are best enforced structurally.** Cleanup, terminal states, and metadata
   preservation are far cheaper to guarantee with types and scope guards than with tests alone.
4. **The dangerous properties are the quiet ones.** 51.8, 51.9, 51.14, and 51.15 fail without an
   exception, so they never appear in your error metrics. Audit them deliberately.
5. **Correctness is per path, not per service.** A service can be correct on every path it has
   tested and still be wrong on the path nobody wrote down. Chapter 52 finds those paths.

## Exercises

1. For each of the 18 properties, name the file in your codebase where it is most likely violated
   — and say why.
2. Pick one property and write the *cheapest* verification you could add this week. Then write the
   most thorough one, and decide which you will actually keep.
3. Instrument an error counter and a terminal-record counter for one operation. The difference is
   your silent-discard rate.
4. Write the "proof line" for each property: the sentence a reviewer can check. Use the checklist in
   [`05-reference/README.md`](./05-reference/README.md).

## Related

- [Chapter 52 — Failure-Path Analysis](../52-failure-path-analysis/README.md)
- [Part XX index](../README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../GLOSSARY.md)
