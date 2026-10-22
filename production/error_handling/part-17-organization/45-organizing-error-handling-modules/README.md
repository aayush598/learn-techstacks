# Chapter 45 — Organizing Error-Handling Modules

> Part XVII · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Part IV — Layered Architecture](../../part-04-architecture/README.md), [Chapter 8 — Error Codes and Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)

## One-sentence summary

Error handling becomes unmaintainable not when the design is wrong, but when primitives, domain
errors, adapters, registries, retry policies, and serialization are placed in **modules that do
not own them** — so this chapter assigns every concern a home and a one-way dependency direction.

## Why this chapter matters

The most common decay path for an error-handling system is organizational, not conceptual: a
`utils/errors.ts` file grows until nobody can find anything, three adapters invent three
translations for the same Postgres error, and a circular import between the registry and the HTTP
layer forces someone to build a "god module" that imports everything. By the time the design is
"wrong" in code review, it has already been wrong in production for two quarters. This chapter
prevents that by making **placement a decision with rules**, not a habit.

## Chapter map

The chapter has 20 sections. They are grouped into five files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-where-error-code-belongs.md`](./01-concepts/01-where-error-code-belongs.md) | 45.1, 45.16 | The placement rule: define where the decision is owned, handle where the fallback is owned |
| [`01-concepts/02-shared-kernel-vs-app-specific.md`](./01-concepts/02-shared-kernel-vs-app-specific.md) | 45.2, 45.15, 45.18 | What goes in the shared kernel, what stays feature-owned, and when a reusable package earns its cost |
| [`01-concepts/03-core-zones-primitives-domain-infra-transport.md`](./01-concepts/03-core-zones-primitives-domain-infra-transport.md) | 45.3–45.6 | The four zones: core primitives, domain definitions, infra adapters, transport handlers |
| [`01-concepts/04-supporting-modules-registries-mappings-retries-serialization.md`](./01-concepts/04-supporting-modules-registries-mappings-retries-serialization.md) | 45.7–45.11 | Registries, mapping modules, retry modules, recovery modules, serialization modules |
| [`01-concepts/05-feature-modules-and-navigability.md`](./01-concepts/05-feature-modules-and-navigability.md) | 45.17, 45.19, 45.20 | Independent feature modules, naming/navigability, the standard directory structure |
| [`02-deep-dive/01-circular-dependency-avoidance.md`](./02-deep-dive/01-circular-dependency-avoidance.md) | 45.12 | Why error modules cycle, and the four techniques that break the cycles |
| [`02-deep-dive/02-avoiding-god-module-and-duplication.md`](./02-deep-dive/02-avoiding-god-module-and-duplication.md) | 45.13, 45.14 | Splitting the god module; extracting shared translation and policy without a new framework |
| [`03-practical-examples/01-acme-error-module-tree.md`](./03-practical-examples/01-acme-error-module-tree.md) | 45.20 (applied) | A complete error-handling directory tree for Acme SaaS with working code |
| [`03-practical-examples/02-extracting-a-feature-owned-error-module.md`](./03-practical-examples/02-extracting-a-feature-owned-error-module.md) | 45.16, 45.17 (applied) | Before/after: moving Checkout errors out of the global file into a feature-owned module |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Placement rules, dependency rules, review checklist |
| [`05-reference/README.md`](./05-reference/README.md) | all | Directory structure reference, module placement decision table, ownership template |

## Learning objectives

By the end you can:

- Point at any error-handling file in a repository and name the rule that put it there.
- Split a shared kernel from feature-owned error definitions and defend the split line.
- Identify the import direction between domain, infra, and transport error modules — and detect
  a cycle before the bundler does.
- Name the module responsible for each of: code registry, translation table, retry policy,
  compensation, and response serialization.

## Key takeaways

1. **Define errors where the failure decision is owned; handle them where the fallback is
   owned.** These are almost never the same module.
2. **The shared kernel holds primitives, not policy.** `AppError`, `Result`, `Category` live in
   the kernel; `CHECKOUT_CARD_DECLINED` lives in Checkout.
3. **Dependencies point inward**: transport → infra → domain → kernel. Never the reverse.
4. **A registry is data, not behavior** — which is exactly what makes it safe to share and safe
   to code-generate from.
5. **Navigability is a feature.** If a new engineer cannot find "where Checkout errors are
   defined" in 30 seconds, the structure has failed regardless of its elegance.

## Exercises

1. Draw your repository's current error-module dependency graph. Mark every edge that points
   outward (toward infra/transport). Each one is a candidate refactor.
2. List every error code your app can emit. Assign each to an owning module. Codes with no owner
   are your first backlog items.
3. Take your biggest `errors.ts` (or equivalent) and split it using the four-zone model. Count
   how many files it becomes — teams typically report 8–20.
4. Find one translation you have written more than once (e.g. Postgres `23505` → conflict).
   Extract it into the adapter module that owns that dependency and delete the duplicates.

## Related

- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../46-error-handling-patterns-and-anti-patterns/README.md)
- [Designing a Layered Error-Handling Architecture](../../part-04-architecture/09-layered-error-handling-architecture/README.md)
- [Reusable Error-Handling Infrastructure](../../part-21-maintainability/54-reusable-error-handling-infrastructure/README.md)
