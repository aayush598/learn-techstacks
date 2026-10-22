# Chapter 54 — Reusable Error-Handling Infrastructure

> Part XXI · _Estimated reading time: 80–100 min_
> **Prerequisite:** [Chapter 53 — Reducing Error-Handling Complexity](../53-reducing-error-handling-complexity/README.md), [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)

## One-sentence summary

Reusable error-handling infrastructure is **a small package with stable interfaces, a
semver promise, and a customization rule** — not a framework, and not a folder of
copy-pasted helpers.

## Why this chapter matters

Most teams that need shared error handling build one of two things, and both fail:

- **A framework.** 3,500 lines, seven new concepts, nine configuration points, one owner
  nobody volunteers to be. It is correct, and it is bypassed within two quarters.
- **A copy-paste folder.** A `shared/errors` directory that every repository clones and then
  diverges from. The divergence is the reason the folder existed.

The version of this that works is narrower than both: **a core library of primitives and
tables, a set of adapters that own vendor-specific translation, and a versioning policy that
makes clear which changes are safe**. Acme's `@acme/errors` package is **1,240 lines** across
**10 modules**, has **zero configuration points**, and was adopted by **11 services**.

## Chapter map

The chapter has 20 sections, grouped into five concept files, two deep-dives, and two
package builds.

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-the-reusable-core-library.md`](./01-concepts/01-the-reusable-core-library.md) | 54.1, 54.2, 54.3, 54.5 | The core type, the factory, the standard interfaces, the standard metadata |
| [`01-concepts/02-mapping-interfaces-and-adapters.md`](./01-concepts/02-mapping-interfaces-and-adapters.md) | 54.4, 54.8, 54.9, 54.10 | The mapping interface, standard boundaries, framework and integration adapters |
| [`01-concepts/03-shared-retry-and-recovery-policies.md`](./01-concepts/03-shared-retry-and-recovery-policies.md) | 54.6, 54.7 | What belongs in a shared retry policy, and what belongs in a shared recovery policy |
| [`01-concepts/04-reusable-api-and-job-handling.md`](./01-concepts/04-reusable-api-and-job-handling.md) | 54.11, 54.12 | One HTTP adapter and one job adapter, reused across services |
| [`01-concepts/05-multiple-frameworks-languages-and-scope.md`](./01-concepts/05-multiple-frameworks-languages-and-scope.md) | 54.13, 54.14, 54.15, 54.19, 54.20 | Multi-framework and multi-language support, the scope limit, the reference architecture |
| [`02-deep-dive/01-versioning-shared-packages-without-breaking-consumers.md`](./02-deep-dive/01-versioning-shared-packages-without-breaking-consumers.md) | 54.16, 54.17 | Semver rules for error packages, the change-classification matrix, the deprecation window |
| [`02-deep-dive/02-starter-template-and-customization-rules.md`](./02-deep-dive/02-starter-template-and-customization-rules.md) | 54.18, 54.19 | The starter template, and the seven customization rules that keep it yours |
| [`03-practical-examples/01-the-acme-errors-package-skeleton.md`](./03-practical-examples/01-the-acme-errors-package-skeleton.md) | 54.1–54.12 (applied) | A complete `@acme/errors` package: core type, factory, mapping interface, retry policies, HTTP adapter, job adapter |
| [`03-practical-examples/02-consuming-and-extending-the-package.md`](./03-practical-examples/02-consuming-and-extending-the-package.md) | 54.11–54.15 (applied) | How three services consume the package and extend it without forking |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules for packages, adapters, and versioning |
| [`05-reference/README.md`](./05-reference/README.md) | all | Infrastructure spec, interface signatures, versioning policy, checklist |

## Learning objectives

By the end you can:

- Design a **core error package** with a stable type, a typed factory, and a total registry —
  and explain why the registry is data rather than behaviour.
- Write a **mapping interface** that a provider adapter implements, so vendor errors become
  categories without the core knowing the vendor.
- Decide what belongs in a **shared retry policy** versus a **service-specific one**, and
  defend the split.
- Build **one HTTP adapter and one job adapter** that both serve every service, with the
  service-specific parts injected.
- Apply **semver rules to an error package**: what is a minor bump, what is a major bump,
  what is a breaking change, and how to deprecate without breaking consumers.
- Ship a **starter template** that a new project adopts in one afternoon.

## Key takeaways

1. **The shared thing is the decision, not the code.** A shared package holds tables and
   interfaces; the *tables* are the value, the *interfaces* are the extension point.
2. **The core knows no vendors.** Adapters translate; the core classifies. If the core
   imports a vendor SDK, every consumer inherits the dependency.
3. **Configuration points are the enemy.** A shared package with nine knobs behaves like
   nine local packages. Extend the data, not the behaviour.
4. **A registry is data, which makes it safe to share.** Behaviour is where shared code
   rots; data is where it scales.
5. **The version number is a promise about blast radius.** Adding a code is a minor bump;
   changing what an existing code means is a major bump, no matter how small the diff.
6. **Adapters are where the value is.** A core with no adapters saves nothing; a core with
   an adapter per provider removes the duplication that motivated it.
7. **Reuse is optional by design.** A service that does not want the package must be able to
   use just the registry table and nothing else.

## Exercises

1. Write the **export surface** of your would-be error package: every exported symbol, its
   type, and one line of purpose. If the list is longer than 25 symbols, cut it.
2. Write a **mapping interface** for one of your vendors, and implement it for two of its
   error shapes. Measure how many lines it removes from the call sites.
3. Classify your last **ten changes** to error handling as additive, behaviour-changing, or
   breaking. If you cannot tell for any of them, you do not have a version policy.
4. Take the reference architecture in this chapter and mark which parts your organisation
   actually needs. The answer is usually 40%.
5. Draft the **deprecation window** you would give a code you are removing, and write the
   release-note line you would publish.

## Related

- [Chapter 53 — Reducing Error-Handling Complexity](../53-reducing-error-handling-complexity/README.md)
- [Chapter 55 — Error-Handling Documentation](../55-error-handling-documentation/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 49 — Error Contract Design and Versioning](../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
