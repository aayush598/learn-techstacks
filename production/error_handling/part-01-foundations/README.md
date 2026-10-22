# Part I — Foundations of Production-Grade Error Handling

> **Chapters 1–3.** Before you can build a taxonomy, a registry, or a resilience policy, you
> need precise language and firm principles. This part builds the mental model everything else
> depends on. Skipping it is the most common reason error handling becomes inconsistent later.

## Learning objectives

By the end of Part I you will be able to:

1. Distinguish **error**, **fault**, **failure**, and **exception** precisely and use the terms
   consistently in code reviews and design docs.
2. Classify any failure along ~15 independent dimensions (expected/unexpected, transient/
   permanent, recoverable/unrecoverable, …) and use those classifications to drive decisions.
3. Articulate the ~20 principles of high-quality error handling and recognize where most codebases
   violate them.
4. Define the error-handling requirements appropriate to a given product stage and architecture
   (MVP, startup, enterprise, multi-tenant, real-time, financial, AI, background).

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 1 | [Understanding Errors and Failures](./01-understanding-errors-and-failures/README.md) | Vocabulary, classification dimensions, failure domains, cost of poor handling |
| 2 | [Principles of High-Quality Error Handling](./02-principles-of-high-quality-error-handling/README.md) | The ~20 principles and how to apply them |
| 3 | [Error-Handling Requirements for a SaaS Product](./03-error-handling-requirements-for-saas/README.md) | Requirements by stage, architecture, and risk profile |

## How to study this part

- Read Chapter 1 fully; do the classification exercises against your own codebase.
- For Chapter 2, keep a list of principles you currently violate. Do not fix them yet.
- For Chapter 3, identify your product stage and write down your required maturity level.

## Key takeaways

- **Errors are information, not emergencies.** Production-grade handling starts by treating an
  error as a message that must be classified, routed, and resolved predictably.
- **Most "error handling bugs" are really classification bugs** — the failure was routed to the
  wrong policy because it was misunderstood.
- **Requirements are contextual.** An MVP does not need a saga orchestrator; a payments SaaS does
  not get to skip idempotency.

## Related

- [Part II — Error Taxonomy and Classification](../part-02-error-taxonomy/README.md)
- [Glossary](../../GLOSSARY.md)
