# Chapter 55 — Error-Handling Documentation

> Part XXI · _Estimated reading time: 75–95 min_
> **Prerequisite:** [Chapter 53 — Reducing Error-Handling Complexity](../53-reducing-error-handling-complexity/README.md), [Chapter 54 — Reusable Error-Handling Infrastructure](../54-reusable-error-handling-infrastructure/README.md)

## One-sentence summary

Error-handling documentation is **a small set of documents that describe behaviour you can
verify** — architecture, categories, the code registry, the public API contract, the policy
tables, ownership, propagation, boundaries, fallbacks, transactional behaviour, limitations,
and a decision guide — each one checked by something mechanical.

## Why this chapter matters

Documentation fails in a specific way: it is written once, under pressure, by the person who
just solved the problem, and it is never checked again. Six months later it is wrong in
exactly the places that matter.

At Acme, the drift was measurable:

| Document | Claim | Code | Discovered |
| -------- | ----- | ---- | --------- |
| `ERRORS.md` | "Retries stop at 3 attempts" | `maxAttempts: 5` in the billing worker | During a duplicate-charge incident |
| `runbook.md` | "A `500` means a bug" | `500` also returned for data-integrity violations | During a paging storm |
| The wiki | "Codes are added to `errors.ts`" | Codes live in `features/*/codes.ts` | On a new engineer's first PR |
| The API guide | "Unknown codes return `500`" | Unknown codes return `502` with `PROVIDER_REJECTED` | By a partner, in production |

None of these were lies when written. Each was true on the day it was written and false
later, with **no signal** that it had gone stale.

The fix is not "write better docs". It is **make every document mechanically checkable**, so
that the day the code changes, the document fails a CI job instead of misleading somebody.

## Chapter map

The chapter has 16 sections, grouped into five concept files, two deep-dives, and two
document sets.

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-the-documentation-set-and-its-layers.md`](./01-concepts/01-the-documentation-set-and-its-layers.md) | 55.1, 55.2, 55.3 | The four layers of the set, how to document categories, how to document the code registry |
| [`01-concepts/02-documenting-external-contracts-and-policies.md`](./01-concepts/02-documenting-external-contracts-and-policies.md) | 55.4, 55.5, 55.6 | The public API error contract, the retry table, the recovery table |
| [`01-concepts/03-ownership-propagation-and-boundaries.md`](./01-concepts/03-ownership-propagation-and-boundaries.md) | 55.7, 55.8, 55.9 | Who owns what, how errors propagate, where translation happens |
| [`01-concepts/04-transactional-failure-limitations-and-exceptions.md`](./01-concepts/04-transactional-failure-limitations-and-exceptions.md) | 55.10, 55.11, 55.12, 55.13 | Fallback behaviour, transactional failure, known limitations, exceptional cases |
| [`01-concepts/05-decision-guides-and-onboarding.md`](./01-concepts/05-decision-guides-and-onboarding.md) | 55.14, 55.15 | The decision guide, and the onboarding guide that gets a new engineer productive in under an hour |
| [`02-deep-dive/01-keeping-docs-aligned-with-behavior.md`](./02-deep-dive/01-keeping-docs-aligned-with-behavior.md) | 55.16 (mechanics) | How drift happens, the four drift types, and the three ways to prevent each |
| [`02-deep-dive/02-doc-drift-detection-and-ci-gates.md`](./02-deep-dive/02-doc-drift-detection-and-ci-gates.md) | 55.16 (enforcement) | The drift checks themselves, their runtime budget, and the CI gate design |
| [`03-practical-examples/01-documentation-set-outline-for-a-new-project.md`](./03-practical-examples/01-documentation-set-outline-for-a-new-project.md) | 55.1–55.15 (applied) | The complete document set for a new service, section by section, with sizes |
| [`03-practical-examples/02-a-filled-error-handling-adr.md`](./03-practical-examples/02-a-filled-error-handling-adr.md) | 55.14–55.16 (applied) | A complete ADR: context, decision, consequences, and the checks that keep it true |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules for writing and maintaining error documentation |
| [`05-reference/README.md`](./05-reference/README.md) | all | Document inventory, templates, drift-check catalog, onboarding checklist |

## Learning objectives

By the end you can:

- Produce a **four-layer documentation set** — architecture, contract, policy, decision — and
  know what belongs in each layer.
- Document the **code registry** so that a new engineer can add a code without asking anyone.
- Write the **public API error contract**, including what happens for a code the client does
  not know.
- Record the **retry and recovery tables** in a form a reader can act on at 3 a.m.
- State **ownership, propagation, and boundary placement** as rules, not as prose.
- Document **known limitations and exceptional cases** — the parts everyone forgets.
- Write a **decision guide** that answers "what should I do when…" in one lookup.
- Get a new engineer from zero to **adding a new error code in under an hour**.
- Detect **documentation drift in CI** with checks that run in under two minutes.

## Key takeaways

1. **A document earns its place only if something checks it.** An unchecked document is a
   memory aid that decays.
2. **Four layers, four audiences.** Architecture for new engineers, the contract for API
   consumers, the policy tables for operators, the decision guide for implementers.
3. **The registry is the centre.** Categories, statuses, retries, and recovery all derive
   from it; document the registry and most of the rest follows.
4. **Document the failure, not the success.** The happy path is obvious; the failure path is
   what a reader needs.
5. **Limitations are the most valuable section.** "This code is not retried because the write
   is not idempotent" saves more time than any amount of prose.
6. **Onboarding is a measurable outcome.** If a new engineer cannot add a code in an hour,
   the documentation is not finished.
7. **Drift detection is cheap.** Every check in this chapter runs in under two minutes
   combined, and the registry check runs in under a second.

## Exercises

1. List every document in your repository that describes error behaviour. For each, name the
   thing that would make it **wrong** and how you would notice.
2. Write the "unknown code" paragraph of your public API contract. If you cannot, your
   contract is incomplete.
3. Time a new colleague on "add a new error code to this service". If it is over an hour,
   find the two documents that are missing.
4. Write the CI check that fails when a registered code is not in the documentation table.
   Measure its runtime on your repository.
5. Write down three **known limitations** of your error handling. If you cannot name three,
   you do not know what your system does not handle.

## Related

- [Chapter 53 — Reducing Error-Handling Complexity](../53-reducing-error-handling-complexity/README.md)
- [Chapter 54 — Reusable Error-Handling Infrastructure](../54-reusable-error-handling-infrastructure/README.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)
