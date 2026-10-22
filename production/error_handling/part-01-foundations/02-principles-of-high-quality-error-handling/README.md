# Chapter 2 — Principles of High-Quality Error Handling

> Part I · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Chapter 1 — Understanding Errors and Failures](../01-understanding-errors-and-failures/README.md)

## One-sentence summary

High-quality error handling is not a library you install but a small set of **principles** —
explicitness, consistency, preservation of cause, and predictable posture — that together make
failure behavior boring, safe, and cheap to maintain.

## Why this chapter matters

Teams rarely fail because they lack a framework; they fail because the *same* failure is handled
five different ways, the original cause is lost, an error is swallowed into a fake success, or a
transient blip is surfaced as a permanent outage. Each of those is a **principle violation**, and
each is cheap to prevent if you agree on the rules before the code exists.

This chapter is the rulebook. Every later chapter — taxonomy, error model, boundaries, retries —
is an application of these principles. When you disagree about a design decision in Chapter 20,
you will usually find the tie-breaker here.

## Chapter map

The chapter has 20 sections grouped into eight files.

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-explicitness-consistency-and-predictability.md`](./01-concepts/01-explicitness-consistency-and-predictability.md) | 2.1, 2.2, 2.3, 2.18 | Why explicit beats implicit, why consistency is a feature, errors as architecture, predictability |
| [`01-concepts/02-structure-separation-and-responsibility.md`](./01-concepts/02-structure-separation-and-responsibility.md) | 2.4, 2.5, 2.6, 2.19, 2.20 | Separating business logic from handling, centralized policy vs local decisions, single responsibility, boilerplate, maintainability |
| [`01-concepts/03-failure-posture-and-defensive-design.md`](./01-concepts/03-failure-posture-and-defensive-design.md) | 2.7, 2.8, 2.9, 2.10, 2.11 | Fail-fast, fail-safe, graceful degradation, defensive vs excessive defense, least surprise |
| [`01-concepts/04-preserving-and-not-swallowing-errors.md`](./01-concepts/04-preserving-and-not-swallowing-errors.md) | 2.12, 2.13, 2.14, 2.15, 2.16, 2.17 | Transparency vs abstraction, preserving cause, avoiding swallowing, failure→success, redundant handling, catch-and-rethrow |
| [`02-deep-dive/01-fail-fast-fail-safe-and-degradation.md`](./02-deep-dive/01-fail-fast-fail-safe-and-degradation.md) | 2.7–2.9 | A decision framework for choosing a failure posture under real constraints |
| [`02-deep-dive/02-implicit-behavior-and-error-erasure.md`](./02-deep-dive/02-implicit-behavior-and-error-erasure.md) | 2.1, 2.4, 2.12–2.17 | The mechanics of how good signals get erased, and edge cases |
| [`03-practical-examples/01-refactoring-toward-the-principles.md`](./03-practical-examples/01-refactoring-toward-the-principles.md) | all | Before/after refactors across the recurring cast |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Do/don't tables, anti-patterns, chapter checklist |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cheat sheet, decision tables, chapter glossary, signposts |

## Learning objectives

By the end you can:

- Explain why **explicit error contracts** beat implicit conventions, and enforce them in review.
- Choose deliberately between **fail-fast, fail-safe, and graceful degradation**.
- Separate **error policy** (central) from **recovery decisions** (local) without creating a god module.
- Preserve the **original cause** through wraps and translations while keeping messages safe.
- Name and reject the seven most common **signal-erasure anti-patterns**.
- Reduce error-handling **boilerplate** without introducing a framework you now must maintain.

## Key takeaways

1. **Every principle here reduces one of two costs:** the cost of *understanding* a failure, or the
   cost of *recovering* from it. Optimize for both, in that order.
2. **Consistency beats cleverness.** A predictable mediocre standard beats ten bespoke "better"
   solutions, because operators and reviewers can only reason about patterns they can recognize.
3. **An error is a first-class artifact.** If it has no owner, no code, and no documented outcome,
   it will be mishandled.
4. **Never convert a failure into a success.** This single rule prevents the most expensive class of
   production bugs: silent corruption.
5. **The best amount of defensive code is the least that makes every failure path safe** — not the
   most, and not none.

## Exercises

1. Pick one endpoint in your product and list every principle it violates; rank by risk.
2. Find every `catch` block in your codebase and mark each as *handle*, *translate*, *rethrow*, or
   *swallow*. Count the swallows.
3. For one optional dependency, decide its posture (fail-fast / fail-safe / degrade) and write the
   one-line justification.
4. Rewrite one function so its failure behavior is explicit in its signature or return type.

## Related

- [Chapter 1 — Understanding Errors and Failures](../01-understanding-errors-and-failures/README.md)
- [Chapter 3 — Error-Handling Requirements for a SaaS Product](../03-error-handling-requirements-for-saas/README.md)
- [Part II — Error Taxonomy and Classification](../../part-02-error-taxonomy/README.md)
- [Glossary](../../GLOSSARY.md)
