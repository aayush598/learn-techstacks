# Part XVII — Error Handling in Architecture and Code Organization

> **Chapters 45–46.** You have designed an error model, a taxonomy, and resilience policies.
> This part answers a different question: *where does the code live?* A perfect taxonomy that
> is copy-pasted into six adapters, or trapped inside a 3,000-line `errors.ts` god module,
> decays within months. Part XVII turns the design into a **maintainable physical layout** and
> names the **patterns and anti-patterns** that layout is meant to enforce.

## Learning objectives

By the end of Part XVII you will be able to:

1. Place every error-handling concern (primitives, domain errors, adapters, registries, retry
   policies, serialization) in the **module that owns it**, with a one-way dependency graph.
2. Draw a boundary between the **shared error kernel** and **feature-owned error code**, and keep
   the kernel small enough to stay stable.
3. Detect and break **circular dependencies** between error modules before they force a god
   module.
4. Recognize the ~12 canonical error-handling patterns (global handler, adapter, result type,
   registry, translation, retry, breaker, fallback, boundary, compensation, fail-fast, fail-safe)
   and select between them deliberately.
5. Spot the ~13 anti-patterns (empty catch, swallow-and-continue, success-shaped failures,
   retry-everything, deep wrappers, overengineering…) in code review and refactor them toward the
   simplest pattern that works.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 45 | [Organizing Error-Handling Modules](./45-organizing-error-handling-modules/README.md) | Where error code belongs, shared kernel vs feature ownership, circular deps, standard directory structure |
| 46 | [Error-Handling Patterns and Anti-Patterns](./46-error-handling-patterns-and-anti-patterns/README.md) | The pattern catalog, the anti-pattern catalog, selection trade-offs, before/after refactors |

## How to study this part

- Chapter 45 is a *map*. Open your own repository alongside it and try to locate each module it
  names. Gaps in the map are your action items.
- Chapter 46 is a *checklist*. Read the patterns first (46.1–46.12, 46.26), then audit your
  codebase against the anti-patterns (46.13–46.25). Most teams find 5–10 live instances of at
  least one anti-pattern in their first audit.
- The practical examples build one concrete layout for the recurring cast — Acme SaaS — that
  you can copy and shrink to fit your project size.

## Key takeaways

- **Organization is policy.** A retry policy duplicated in four call sites is an organizational
  defect that *becomes* a retry-storm defect. Structure prevents the failure mode before any
  runtime check can.
- **Dependencies point inward.** Domain error definitions never import infra; adapters translate
  *toward* the domain. Every circular error dependency is a design smell with a runtime cost.
- **Own every code.** An error code with no owning module is an error code no one dares deprecate.
- **The simplest pattern that satisfies the requirement wins.** A typed error thrown and caught
  at the HTTP boundary is production-grade. A generic error-pipeline framework wrapping it usually
  is not.

## Related

- [Part XVI — Specialized SaaS Error Scenarios](../part-16-specialized-saas-scenarios/README.md)
- [Part XXI — Error Handling for Maintainability](../part-21-maintainability/README.md)
- [Glossary](../../GLOSSARY.md)
