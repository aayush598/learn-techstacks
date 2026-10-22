# Chapter 8 — Error Codes and Error Registries

> Part III · _Estimated reading time: 70–85 min_
> **Prerequisite:** [Chapter 6 — Designing the Application's Error Model](../06-designing-the-applications-error-model/README.md)

## One-sentence summary

An **error code** is the stable, machine-readable name for a condition, and an **error registry**
is the single source of truth that maps every code to its category, HTTP status, retry policy, user
message, and client action — so no consumer ever guesses.

## Why this chapter matters

Codes are the part of an error that other systems depend on: the API layer maps them to status
codes, the frontend maps them to messages and actions, the retry engine maps them to policies,
and support maps them to runbooks. When codes are missing, unstable, duplicated, or undocumented,
every one of those mappings drifts. A registry turns a pile of constants into a **governed
contract** — and makes "we added a code but forgot to map it" a detectable event rather than a
production surprise.

## Chapter map

The chapter has 18 sections. They are grouped into eight files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-why-codes-and-stable-identifiers.md`](./01-concepts/01-why-codes-and-stable-identifiers.md) | 8.1–8.2, 8.17 | Why codes exist; stability; avoiding implementation-derived codes |
| [`01-concepts/02-code-naming-and-scoping.md`](./01-concepts/02-code-naming-and-scoping.md) | 8.3–8.5 | Naming conventions; domain-prefixed vs global; internal vs public |
| [`01-concepts/03-uniqueness-and-registry-structure.md`](./01-concepts/03-uniqueness-and-registry-structure.md) | 8.6–8.9 | Uniqueness, collision prevention, centralized vs domain-owned registries |
| [`01-concepts/04-mapping-codes-to-behavior.md`](./01-concepts/04-mapping-codes-to-behavior.md) | 8.10–8.14 | Documentation; mapping to HTTP, client actions, retries, user messages |
| [`01-concepts/05-deprecation-compatibility-and-detection.md`](./01-concepts/05-deprecation-compatibility-and-detection.md) | 8.15–8.16, 8.18 | Deprecating codes, backward compatibility, detecting undocumented codes |
| [`02-deep-dive/01-registry-as-code-and-collision-testing.md`](./02-deep-dive/01-registry-as-code-and-collision-testing.md) | 8.6–8.8, 8.18 | Enforcing the registry in CI; collision and coverage tests |
| [`02-deep-dive/02-backward-compatibility-and-deprecation.md`](./02-deep-dive/02-backward-compatibility-and-deprecation.md) | 8.15–8.16 | Migration mechanics for codes across versions and clients |
| [`03-practical-examples/01-sample-error-registry.md`](./03-practical-examples/01-sample-error-registry.md) | 8.1–8.18 | A sample registry table plus TypeScript enforcement |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cheat sheet, decision tables, glossary |

## Learning objectives

By the end you can:

- Write stable codes that survive refactors and never encode implementation detail.
- Choose a naming and scoping convention (domain-prefixed, globally unique, internal vs public).
- Build a registry that maps each code to HTTP status, retry policy, client action, and message.
- Guarantee uniqueness and detect undocumented/colliding codes automatically in CI.
- Deprecate and remove codes without breaking old clients.

## Key takeaways

1. **Codes are the contract; messages are not.**
2. **Stable and append-only.** Repurposing or renaming a code is a breaking change.
3. **One meaning per code, everywhere.** Uniqueness is enforced, not assumed.
4. **The registry is executable.** HTTP, retry, action, and message all derive from it.
5. **Deprecate, never repurpose.** Retire codes through a documented lifecycle.

## Exercises

1. List every error code in your codebase; note how many are undocumented or duplicated.
2. Design a `domain.action` naming scheme for your product and rename five codes.
3. Add a CI test that fails if a code is thrown but missing from the registry.

## Related

- [Chapter 6 — Designing the Application's Error Model](../06-designing-the-applications-error-model/README.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../07-error-classes-types-and-structured-results/README.md)
- [Chapter 20 — Standardized API Error Responses](../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
