# Part XIX — Error Contracts, Compatibility, and Governance

> **Chapters 49–50.** Everything before this part builds an error-handling *system*. This part
> turns that system into a **contract** that survives change — and into an **engineering
> standard** that keeps every team in the company pointed the same way. A system that works
> today but drifts every quarter is not production-grade.

## Learning objectives

By the end of Part XIX you will be able to:

1. Name the **five contract surfaces** an error crosses (internal, module, service,
   backend↔frontend, public API) and assign a **stability tier** to each.
2. Classify any error-contract change as **additive** or **breaking**, and pick the right
   mechanism (new code, alias, dual-emit, deprecation window, major version).
3. Write and enforce **backward** and **forward** compatibility rules, including how
   consumers must behave when they meet an **unknown code**.
4. Run a full **deprecation lifecycle**: introduce → dual-emit → measure → sunset → remove,
   gated on consumption telemetry rather than opinion.
5. Version an **error contract independently** of the API version and the package version,
   using semver semantics that match the actual blast radius of a change.
6. Write an **org-wide error-handling standard** with normative rules, a documented exceptions
   register, and an adoption path that does not require a rewrite.
7. Keep a standard **practical**: enforce the rules that are objectively checkable, leave
   judgement calls to review, and retire rules that no longer earn their keep.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 49 | [Error Contract Design and Versioning](./49-error-contract-design-and-versioning/README.md) | Surfaces, stability tiers, compatibility rules, deprecation mechanics, contract versioning |
| 50 | [Error Handling as an Engineering Standard](./50-error-handling-as-an-engineering-standard/README.md) | Org-wide conventions, normative rules, security requirements, exceptions, governance, rollout |

## How to study this part

- Chapter 49 is about **one contract**. Chapter 50 is about **the set of rules that keeps many
  contracts consistent**. Read 49 first.
- Before reading Chapter 49, re-read the compatibility matrix in
  [Chapter 8 — Error Codes and Error Registries](../part-03-error-models/08-error-codes-and-error-registries/README.md).
  Chapter 49 operates at the *surface* level: what a consumer may rely on, not just what a
  registry row says.
- While reading Chapter 50, keep a real codebase open. For every rule, ask: *could we
  mechanically check this?* If yes, it belongs in CI. If not, it belongs in review.
- The practical files are the point of this part. Read
  [the deprecation workflow](./49-error-contract-design-and-versioning/03-practical-examples/01-deprecation-workflow-introduce-dual-emit-sunset.md)
  and [the standard excerpt](./50-error-handling-as-an-engineering-standard/03-practical-examples/01-org-error-handling-standard-excerpt.md)
  as templates for your own organisation.

## Key takeaways

- **An error contract is a set of promises about failure**, not a set of error codes. The codes
  are the vocabulary; the contract is what consumers may rely on.
- **Classify every change before shipping it.** Additive changes ship freely; reductive and
  repurposing changes are versioned migrations.
- **Compatibility has two directions.** Backward (new consumer reads old producer) and forward
  (old consumer survives new producer). The second one is the one teams forget.
- **Unknown codes are inevitable.** A consumer that throws on an unrecognised code fails on the
  day you add a new one.
- **Deprecate on telemetry, not on opinion.** "We announced it" is not evidence that anyone
  is listening.
- **Messages are not contract.** Codes and `type` URIs are; wording is not.
- **A standard without exceptions is propaganda.** A standard without enforcement is a
  suggestion. A standard needs both a rule set and a documented escape hatch.
- **Rigidity is a failure mode.** Enforce the rules that are objectively checkable; let review
  handle the rest; and delete rules that stop paying for themselves.

## Where this part sits

```text
Part I–XVIII   Foundations → taxonomy → models → architecture → … → frameworks
    │
    ▼
Part XIX  Contracts & Governance   ◀── you are here
    │
    ├──▶ Part XX–XXII  Correctness, failure-path analysis, design trade-offs
    └──▶ Part XXIII–XXIV  Special cases and the repeatable blueprint
```

Earlier parts define **what** an error is and **where** it is handled. This part defines **what
others may rely on** and **how the organisation keeps that promise**. Part XXIV then folds
these rules into the blueprint that new projects start from.

## Related

- [Part XVIII — Error Handling Across Languages and Frameworks](../part-18-languages-and-frameworks/README.md)
- [Chapter 8 — Error Codes and Error Registries](../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 20 — Standardized API Error Responses](../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Glossary: error code, error registry, Problem Details](../GLOSSARY.md)
