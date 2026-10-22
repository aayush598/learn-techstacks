# Chapter 50 — Error Handling as an Engineering Standard

> Part XIX · _Estimated reading time: 85–100 min_
> **Prerequisite:** [Chapter 49 — Error Contract Design and Versioning](../49-error-contract-design-and-versioning/README.md)

## One-sentence summary

An **engineering standard** turns error handling from something each team negotiates into
something the organisation **publishes, enforces, and changes on purpose** — with written
rules, a documented exceptions register, and a change process that keeps the rules honest.

## Why this chapter matters

Chapter 49 made one contract safe. An organisation has hundreds: a public API, a mobile app, a
billing service, six internal libraries, three webhook surfaces, and whatever the fourth team
will build next quarter. Left alone, each of them evolves by local improvisation, and the
organisation accumulates:

- **Four names for the same condition** (`USER_NOT_FOUND`, `USER_DOES_NOT_EXIST`,
  `ACCOUNT_MISSING`, `NO_SUCH_USER`) — the duplication Chapter 8 exists to prevent, returning
  at the organisation level.
- **Four retry postures** — one team retries `409`, another retries `503`, a third retries
  everything, and a fourth retries nothing.
- **Four redaction policies** — and one of them leaks a customer's email in an error message.
- **Four ways to format an error response** — so a frontend must branch four times.

A standard is the mechanism that prevents this. But a standard is also a **trap**: written
without restraint, it becomes a 200-page document nobody reads, full of rules that cannot be
checked, enforced by a linter that blocks legitimate work. Teams then route around it, and the
organisation ends up with a standard it ignores — worse than no standard, because it consumes
attention while providing nothing.

This chapter is about writing a standard that survives contact with real engineers.

## Chapter map

The chapter has 14 sections grouped into seven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-what-a-standard-contains.md`](./01-concepts/01-what-a-standard-contains.md) | 50.1–50.3 | Org-wide conventions, naming standards, code conventions |
| [`01-concepts/02-behavioral-standards.md`](./01-concepts/02-behavioral-standards.md) | 50.4–50.7 | Propagation, retry/timeout, response format, recovery conventions |
| [`01-concepts/03-security-and-exceptions.md`](./01-concepts/03-security-and-exceptions.md) | 50.8–50.9 | Security requirements; the exceptions register |
| [`02-deep-dive/01-durable-vs-ceremonial-rules.md`](./02-deep-dive/01-durable-vs-ceremonial-rules.md) | 50.9, 50.11–50.12 | Which rules survive review, the recorded exception, and avoiding rigidity |
| [`03-practical-examples/01-standards-and-adr-templates.md`](./03-practical-examples/01-standards-and-adr-templates.md) | 50.1–50.8, 50.10 | A standard excerpt with numbered rules, and the ADR template |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | 50.13–50.14, cross-cutting | The reusable playbook, one standard across projects, rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | 50.1–50.12 (quick lookup) | Rule catalogue, templates, decision tables, glossary |

## Learning objectives

By the end you can:

- Write an org-wide standard as a **small set of enforceable rules** plus guidance, not a
  novel.
- Use **normative language** (MUST / MUST NOT / SHOULD / MAY) so that compliance is decidable.
- Specify the conventions for **naming, codes, propagation, retry/timeout, response format,
  recovery, and security** without prescribing implementations.
- Run an **exceptions register** that documents, owns, and expires deviations.
- Record **decisions** as ADRs and manage the standard through a **change process**.
- Apply the same standard across **different stacks** (TypeScript, Python, Go) without
  rewriting it per project.
- Roll a standard out to a **legacy codebase** in phases, without a rewrite.

## Key takeaways

1. **A standard is a contract with your own engineers.** Write it as promises, not as advice.
2. **Rules must be checkable.** If you cannot enforce it mechanically, keep it short and
   label it guidance.
3. **Specify behaviour, not implementation.** The same rule must hold in TypeScript, Python,
   and Go.
4. **Exceptions are a feature.** A standard with no escape hatch gets violated in secret;
   a standard with a documented register gets improved.
5. **Every exception expires.** An exception without a review date is a permanent hole.
6. **Standards age.** Version it, changelog it, retire rules that stop paying for themselves.
7. **Reuse the playbook, not the code.** The blueprint travels; the implementation is local.

## Exercises

1. Write **five** rules for your organisation that could each be enforced by a CI check. Then
   write five you would not — and label the second set "guidance".
2. Audit one team's error handling against the standard you would write. Count the deviations
   and classify each as a *rule violation* or a *context gap* (a place where the standard did
   not anticipate the situation).
3. Draft an **exceptions register** with three columns: rule, exception, owner, review date.
4. Write an ADR that adopts a standard and states what it explicitly does **not** cover.
5. Take the five rules from exercise 1 and implement them as **five CI checks** in a toy
   repository. Measure how long the pipeline takes before and after.

## Related

- [Chapter 49 — Error Contract Design and Versioning](../49-error-contract-design-and-versioning/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
