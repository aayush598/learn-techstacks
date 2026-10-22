# Chapter 30 — Graceful Degradation and Fallbacks

> Part XI · _Estimated reading time: 80–100 min_
> **Prerequisite:** [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../29-timeouts-circuit-breakers-and-bulkheads/README.md)

## One-sentence summary

Graceful degradation is the **deliberate trade of completeness for availability**: when a dependency
fails, you serve a correct-but-reduced result, disable non-essential features, and tell the caller what
is missing — instead of failing the whole request or silently returning wrong data.

## Why this chapter matters

Once retries, timeouts, and breakers have done their job, something still has to decide what the user
sees. That decision is a product decision as much as an engineering one. A checkout that silently
marks an unpaid order as paid is far worse than one that shows "payment temporarily unavailable." A
dashboard that quietly serves week-old data as live is worse than one that labels it stale. This
chapter gives you the vocabulary — required vs optional, fail-open vs fail-closed, stale vs
unavailable, partial features, fallback chains — and the rules to keep degradation honest.

## Chapter map

The chapter has 15 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-principles-and-required-vs-optional.md`](./01-concepts/01-principles-and-required-vs-optional.md) | 30.1, 30.2 | Principles of degradation, classifying required vs optional capabilities |
| [`01-concepts/02-fallback-responses-and-cached-fallbacks.md`](./01-concepts/02-fallback-responses-and-cached-fallbacks.md) | 30.3–30.5 | Fallback responses, cached fallbacks, stale vs unavailable |
| [`01-concepts/03-partial-features-degraded-mode-and-disabling.md`](./01-concepts/03-partial-features-degraded-mode-and-disabling.md) | 30.6–30.8 | Partial features, disabling non-essential work, degraded mode |
| [`01-concepts/04-fallback-failure-silent-inaccuracy-and-communication.md`](./01-concepts/04-fallback-failure-silent-inaccuracy-and-communication.md) | 30.10–30.12 | Fallback failure, avoiding silent inaccuracy, communicating degradation |
| [`01-concepts/05-fail-closed-vs-open-and-cascading.md`](./01-concepts/05-fail-closed-vs-open-and-cascading.md) | 30.13–30.15 | Fail-closed vs fail-open, avoiding cascading fallbacks, eligibility rules |
| [`02-deep-dive/01-fallback-chains.md`](./02-deep-dive/01-fallback-chains.md) | 30.3–30.9 | Designing ordered fallback chains, budgets, and short-circuits |
| [`02-deep-dive/02-fail-open-vs-closed.md`](./02-deep-dive/02-fail-open-vs-closed.md) | 30.10–30.15 | A decision framework with correctness, safety, and reversibility |
| [`03-practical-examples/01-degraded-mode-for-acme.md`](./03-practical-examples/01-degraded-mode-for-acme.md) | 30.1–30.15 | Acme's degraded-mode matrix and implementation |
| [`03-practical-examples/02-fallback-chain-llm-summary.md`](./03-practical-examples/02-fallback-chain-llm-summary.md) | 30.3–30.11 | A cached → smaller-model → template fallback chain for `AgentRun` |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules, anti-patterns, review checklist |
| [`05-reference/README.md`](./05-reference/README.md) | all | Mode matrix, status/header conventions, decision guides |

## Learning objectives

By the end you can:

- Classify every capability as required, important, or optional.
- Choose between a fallback response, a cached value, and an explicit error.
- Design a fallback chain with budgets, timeouts, and loop protection.
- Decide fail-open vs fail-closed from correctness and safety, not habit.
- Disable non-essential work under load without breaking the contract.
- Communicate degradation to users, callers, and dashboards.

## Key takeaways

1. **Degrade deliberately, never accidentally.** Every fallback is a documented decision.
2. **Required capabilities fail closed; optional ones may fail open.** Write the list down.
3. **A fallback must be correct, not just available.** Wrong data is worse than no data.
4. **Stale data must be labelled stale.** Include its age and source.
5. **Fallback chains need budgets and terminal states**, or they cascade.
6. **Silent inaccuracy is the worst outcome** — worse than a visible error.
7. **Degradation is an interface**: status, headers, UI copy, and metrics agree.

## Exercises

1. Classify five features of a system you know as required/important/optional and choose a mode for each.
2. Design a fallback chain for an LLM summary with a 10s user budget.
3. Add a `Degraded` header and a UI banner to an existing endpoint.
4. Simulate a cache outage and confirm the system does not fall back to an unbounded live query.
5. Write eligibility rules for a fallback that must not run for certain tenants or operations.

## Related

- [Chapter 27 — Retry Policies](../27-retry-policies/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
- [Glossary](../../GLOSSARY.md)
