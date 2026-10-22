# Part II — Error Taxonomy and Classification

> **Chapters 4–5.** Once you have precise vocabulary (Part I), the next decision is *how you sort
> failures*. A taxonomy is the shared vocabulary that turns "something went wrong" into a small,
> named set of categories — and every category maps to a policy. Get this wrong and every later
> chapter (retry, HTTP status, security, jobs) inherits the confusion.

## Learning objectives

By the end of Part II you will be able to:

1. Explain **why a taxonomy is an architectural asset**, not a documentation exercise.
2. Design a **hierarchical classification** (family → category → specific condition) that stays
   small as the product grows.
3. Classify any error along **fifteen practical axes**: origin, severity, recoverability,
   permanence, affected component, user impact, retry eligibility, HTTP semantics,
   domain/capability, security implications, transactional consequences, dependency, and
   compensation requirement.
4. Decide when categories should be **mutually exclusive** and when they may intentionally
   **overlap**, and how to choose a **primary axis** for routing.
5. Prevent **category growth** and assign **ownership and governance** so the taxonomy ages well.
6. Recognize and handle the **35 concrete error categories** every SaaS encounters, with real
   codes (HTTP `409`, SQLSTATE `23505`, gRPC `DEADLINE_EXCEEDED`).

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 4 | [Designing a Comprehensive Error Taxonomy](./04-designing-a-comprehensive-error-taxonomy/README.md) | Why taxonomies exist, hierarchical design, the classification axes, governance |
| 5 | [Error Categories in Detail](./05-error-categories-in-detail/README.md) | All 35 categories grouped by family, with codes, policies, and examples |

## How to study this part

- Read Chapter 4 first: it gives you the *axes*. Then read Chapter 5: it gives you the *values*.
- While reading Chapter 5, map each category to a category in **your own** system. Note the gaps.
- Keep the [Chapter 4 reference cheat-sheet](./04-designing-a-comprehensive-error-taxonomy/05-reference/README.md)
  and the [Chapter 5 reference table](./05-error-categories-in-detail/05-reference/README.md) open.
- Do the classification drills in Chapter 5 against real incident tickets.

## Key takeaways

- **A taxonomy is a contract.** It guarantees the same failure is classified the same way in every
  handler, service, and language.
- **Categories are not messages.** Classify by *cause and consequence*, never by the text of an
  error string.
- **Systems route on categories, not on errors.** The taxonomy is what lets a global handler,
  a retry policy, and an alert rule agree without knowing your domain.
- **Small and stable beats complete and sprawling.** Start with ~12–20 families, not 200 codes.
- **Every category needs an owner.** An unowned category is one that silently drifts.

## Where this part sits

```text
Part I  Foundations (vocabulary, principles, requirements)
   │
   ▼
Part II Taxonomy + Categories   ◀── you are here
   │
   ├──▶ Part III Error models, classes, codes, registries
   ├──▶ Part IV  Architecture, boundaries, lifecycle
   └──▶ Parts VIII–XVI  HTTP, DB, external, jobs, security...
```

The taxonomy defined here is *represented* in Part III (models and codes) and *applied* from Part
IV onward. When Part III asks "what fields does an error carry?", the answer is "the ones this
part tells you to classify."

## Related

- [Part I — Foundations](../part-01-foundations/README.md)
- [Part III — Error Models and Representation](../part-03-error-models/README.md)
- [Glossary: error taxonomy, error code](../GLOSSARY.md)
