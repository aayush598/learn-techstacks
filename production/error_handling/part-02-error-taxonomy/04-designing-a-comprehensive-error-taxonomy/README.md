# Chapter 4 — Designing a Comprehensive Error Taxonomy

> Part II · _Estimated reading time: 50–70 min_
> **Prerequisite:** [Chapter 1 — Understanding Errors and Failures](../../part-01-foundations/01-understanding-errors-and-failures/README.md)

## One-sentence summary

An **error taxonomy** is a deliberate, hierarchical classification of every failure a system can
produce — organized along independent axes so that any error, anywhere in the codebase, maps to
the *same* category and therefore the *same* policy.

## Why this chapter matters

Without a taxonomy, "handling an error" means reading its message string and guessing. One
developer retries a `409`, another does not; one returns `500` for a business rule, another `422`;
one logs at `error`, another swallows. Teams then pay for this in retried invalid writes, wrong
HTTP contracts, and alert fatigue. A taxonomy converts subjective judgment into a shared,
reviewable, testable decision — and every later chapter depends on it.

## Chapter map

Chapter 4 has 18 sections, grouped into six files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-why-a-taxonomy.md`](./01-concepts/01-why-a-taxonomy.md) | 4.1, 4.2 | Why every codebase needs a taxonomy; hierarchical classification |
| [`01-concepts/02-classification-axes-origin-through-retry.md`](./01-concepts/02-classification-axes-origin-through-retry.md) | 4.3–4.9 | By origin, severity, recoverability, permanence, component, user impact, retry eligibility |
| [`01-concepts/03-classification-axes-http-through-compensation.md`](./01-concepts/03-classification-axes-http-through-compensation.md) | 4.10–4.15 | By HTTP semantics, domain, security, transaction, dependency, compensation |
| [`01-concepts/04-mutual-exclusivity-growth-governance.md`](./01-concepts/04-mutual-exclusivity-growth-governance.md) | 4.16–4.18 | Mutually exclusive vs overlapping; preventing growth; ownership & governance |
| [`02-deep-dive/01-multi-axis-classification-model.md`](./02-deep-dive/01-multi-axis-classification-model.md) | 4.2–4.16 | How one error occupies many axes; primary axis; precedence rules |
| [`02-deep-dive/02-taxonomy-governance-and-evolution.md`](./02-deep-dive/02-taxonomy-governance-and-evolution.md) | 4.17, 4.18 | Evolving the taxonomy safely; review process; deprecation |
| [`03-practical-examples/01-acme-error-taxonomy.md`](./03-practical-examples/01-acme-error-taxonomy.md) | all | A complete worked taxonomy for Acme SaaS |
| [`03-practical-examples/02-classifying-errors-in-code.md`](./03-practical-examples/02-classifying-errors-in-code.md) | 4.3–4.15 | Classifying errors in code with a real classifier |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Big taxonomy cheat-sheet, axis decision table, glossary |

## Learning objectives

By the end you can:

- Justify the cost of not having a taxonomy with concrete failure scenarios.
- Draw a hierarchy: **family → category → specific condition**.
- Place any error on all fifteen classification axes within a minute.
- Choose the **primary axis** used for routing, retry, and disclosure.
- Decide whether a new category is needed or whether an existing one subsumes it.
- Assign ownership and a governance process so the taxonomy does not rot.

## Key takeaways

1. **A taxonomy is the interface between detection and policy.** Classification is the single
   input every handler, retry rule, and status-code mapper consumes.
2. **Multiple axes, one primary.** An error sits at a point in multi-dimensional space, but each
   context names one **primary axis** for routing.
3. **Prefer origin + domain + recoverability** as the default primary axes; derive HTTP and retry
   from them rather than hand-picking status codes per endpoint.
4. **Growth is the main risk.** Add a category only when an existing one cannot express the
   *policy difference*.
5. **Governance is what keeps it alive.** Every category has an owner, a documented meaning, and
   a deprecation path.

## Exercises

1. List every distinct `throw`/error return in one service. Group them into families.
2. Pick three recent production incidents and classify each on all fifteen axes.
3. Identify two errors currently treated identically that should have different policies.
4. Name the owner for each family you defined.

## Related

- [Chapter 5 — Error Categories in Detail](../05-error-categories-in-detail/README.md)
- [Part III — Error Models and Representation](../../part-03-error-models/README.md)
- [Glossary: error taxonomy, error code](../../GLOSSARY.md)
