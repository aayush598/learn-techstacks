# Chapter 3 — Error-Handling Requirements for a SaaS Product

> Part I · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 2 — Principles of High-Quality Error Handling](../02-principles-of-high-quality-error-handling/README.md)

## One-sentence summary

Error-handling requirements are **contextual**: they follow from your product stage, architecture,
and risk profile — an MVP needs explicit errors and a clean boundary, a financial multi-tenant SaaS
needs idempotency, isolation, and audit — and you should build to the **maturity level your risks
justify**, never more or less.

## Why this chapter matters

Most error-handling pain is a **mismatch**: an MVP burdened with a saga orchestrator, or a payments
platform still returning `200 {"error": true}`. Both are expensive — one in velocity, the other in
lost money and trust. This chapter gives you a way to read a product's context and derive the
`requirements it actually needs`, so you can invest in the right safeguards at the right time.

The recurring theme: **the simplest design that satisfies the requirement**. Not the most
impressive, not the most minimal — the *appropriate* one.

## Chapter map

The chapter has 12 sections grouped into eight files.

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-requirements-by-product-stage.md`](./01-concepts/01-requirements-by-product-stage.md) | 3.1, 3.2, 3.3 | What changes from MVP → growing startup → enterprise SaaS |
| [`01-concepts/02-requirements-by-architecture-and-risk-profile.md`](./01-concepts/02-requirements-by-architecture-and-risk-profile.md) | 3.4, 3.5, 3.6, 3.7, 3.8, 3.9 | Multi-tenant, high-availability, financial, AI, real-time, background processing |
| [`01-concepts/03-balancing-and-choosing-your-maturity-level.md`](./01-concepts/03-balancing-and-choosing-your-maturity-level.md) | 3.10, 3.11, 3.12 | Reliable vs fast vs simple, avoiding premature abstraction, defining maturity |
| [`02-deep-dive/01-multi-tenancy-isolation-and-high-availability.md`](./02-deep-dive/01-multi-tenancy-isolation-and-high-availability.md) | 3.4, 3.5 | Failure domains per tenant, noisy neighbors, blast radius, SLOs |
| [`02-deep-dive/02-choosing-a-maturity-level-without-over-engineering.md`](./02-deep-dive/02-choosing-a-maturity-level-without-over-engineering.md) | 3.10, 3.11, 3.12 | A maturity ladder and how to move one rung at a time |
| [`03-practical-examples/01-acme-requirements-across-stages.md`](./03-practical-examples/01-acme-requirements-across-stages.md) | 3.1–3.3 | Acme SaaS at MVP, startup, and enterprise |
| [`03-practical-examples/02-specialized-saas-requirements-in-code.md`](./03-practical-examples/02-specialized-saas-requirements-in-code.md) | 3.4–3.9 | Requirements expressed as code for each specialized profile |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Do/don't tables, anti-patterns, chapter checklist |
| [`05-reference/README.md`](./05-reference/README.md) | all | Requirement matrix, maturity ladder, glossary, signposts |

## Learning objectives

By the end you can:

- Derive error-handling **requirements** from a product's stage and architecture.
- Decide what an **MVP can safely defer** and what it must never skip.
- Recognize the extra obligations of **multi-tenant, financial, real-time, AI, and background**
  products.
- Place your team on a **maturity ladder** and choose the next rung.
- Balance **reliability, speed, and complexity** without over-engineering.
- Identify and avoid **premature abstraction**.

## Key takeaways

1. **Requirements are derived, not aspirational.** Read stage + architecture + risk, then decide.
2. **A few safeguards are stage-independent:** explicit errors, one boundary, no silent failures,
   correlation IDs, and never faking success.
3. **Every specialized profile adds a specific obligation:** isolation (multi-tenant), idempotency
   (financial), deadlines (real-time), bounded retries (background), provider abstraction (AI).
4. **Maturity is earned by incidents and risk**, not by ambition. Move one rung when a concrete
   failure proves you need it.
5. **Premature abstraction is itself a reliability risk** — untested infrastructure fails too.

## Exercises

1. Write your product's stage, architecture, and top three risks; derive five required safeguards.
2. List which safeguards you have *deferred* and why; mark any that are actually non-negotiable.
3. Place your team on the maturity ladder (`05-reference`) and name the next rung.
4. For one specialized profile you operate, name its specific obligation and whether you meet it.

## Related

- [Chapter 1 — Understanding Errors and Failures](../01-understanding-errors-and-failures/README.md)
- [Chapter 2 — Principles of High-Quality Error Handling](../02-principles-of-high-quality-error-handling/README.md)
- [Part II — Error Taxonomy and Classification](../../part-02-error-taxonomy/README.md)
- [Chapter 61 — Error-Handling Maturity Model](../../part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)
- [Glossary](../../GLOSSARY.md)
