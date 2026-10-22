# Chapter 53 — Reducing Error-Handling Complexity

> Part XXI · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md), [Chapter 46 — Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)

## One-sentence summary

Error-handling complexity is **measured duplication of decisions** — and the fix is to remove
repeated decisions, not to add a framework that hides them.

## Why this chapter matters

The most expensive sentence in a code review is *"why is this mapped differently here?"*. It
means two decision sites exist for one question, one of them is wrong, and the reviewer has to
guess which. This chapter gives you the tools to find those decision sites, decide which ones
deserve to be shared, and keep the change cost of adding an error or a provider to one place.

The trap on both sides is real. Under-abstracted error handling costs **review time** and
produces **silent inconsistencies**. Over-abstracted error handling costs **debug time** and
produces a framework nobody dares touch. Both look like "we need to standardise" from inside
the team, and both are wrong about half the time.

## Chapter map

The chapter has 16 sections, grouped into five concept files, two deep-dives, and two worked
refactors.

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-finding-and-measuring-repetition.md`](./01-concepts/01-finding-and-measuring-repetition.md) | 53.1, 53.7 | How to find duplicated decisions, how to count them, and when duplication is acceptable |
| [`01-concepts/02-extracting-policies-without-over-abstraction.md`](./01-concepts/02-extracting-policies-without-over-abstraction.md) | 53.2, 53.3, 53.16 | What a "policy" is, how to extract one, and how to avoid extracting the wrong one |
| [`01-concepts/03-simplifying-conditionals-translation-and-retries.md`](./01-concepts/03-simplifying-conditionals-translation-and-retries.md) | 53.4, 53.5, 53.6, 53.8 | Replacing nested branches with decision tables; one translation, one retry rule, one fallback |
| [`01-concepts/04-localizing-decisions-and-conventions.md`](./01-concepts/04-localizing-decisions-and-conventions.md) | 53.9, 53.10, 53.11, 53.12 | Making decisions findable, predictable, and cheap to extend |
| [`01-concepts/05-readable-business-logic-and-the-easy-path.md`](./01-concepts/05-readable-business-logic-and-the-easy-path.md) | 53.13, 53.14, 53.15 | Keeping business logic readable and making the correct path the default |
| [`02-deep-dive/01-abstraction-cost-analysis.md`](./02-deep-dive/01-abstraction-cost-analysis.md) | 53.3, 53.16 | The cost model: what an abstraction costs, what it saves, and the break-even test |
| [`02-deep-dive/02-when-abstractions-earn-their-cost.md`](./02-deep-dive/02-when-abstractions-earn-their-cost.md) | 53.2, 53.16 | Six real extractions, scored — including the two that were reverted |
| [`03-practical-examples/01-reducing-repetition-in-checkout.md`](./03-practical-examples/01-reducing-repetition-in-checkout.md) | 53.1, 53.5, 53.6, 53.7 | A before/after refactor of Checkout's four duplicated mapping blocks |
| [`03-practical-examples/02-a-complexity-budget-for-a-feature.md`](./03-practical-examples/02-a-complexity-budget-for-a-feature.md) | 53.9, 53.13, 53.15 | Setting and enforcing a per-feature complexity budget (`ExportJob`) |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules for extraction, simplification, and the anti-patterns of "standardisation" |
| [`05-reference/README.md`](./05-reference/README.md) | all | Measurement worksheet, decision tables, break-even thresholds, review checklist |

## Learning objectives

By the end you can:

- Produce a **duplication report** for a codebase: which decisions exist in more than one place,
  how many copies, and what each copy costs.
- Run an **abstraction cost analysis** and state a verdict — extract, defer, or reject — with
  numbers attached.
- Replace a nested `if`/`else` error branch with a **decision table** that a reviewer can read
  in one screen.
- Explain, in one sentence, where a given policy lives, and add a new error code or a new
  provider by changing **one** file.
- Set a **complexity budget** for a feature and enforce it mechanically.

## Key takeaways

1. **Duplication is the unit of measurement.** "This file is long" is not a finding;
   "this mapping exists in four places" is.
2. **Three copies is the trigger, not the goal.** Two copies often tolerate divergence; the
   third is where the drift becomes a defect.
3. **Extract a decision, not a code block.** A shared `mapPgError()` is worth less than a shared
   *policy* that says what a unique violation means for the whole system.
4. **A policy is a table, and a table is data.** Tables are reviewable, diffable, and
   exhaustively checkable; branches are none of those.
5. **One decision site per question.** If "what does a timeout mean?" is answered in the
   transport layer and the worker, one of them is a guess.
6. **The change cost is the real metric.** "How many files must I touch to add a new error?"
   is the number that predicts whether your conventions are followed.
7. **Some duplication is cheaper than the wrong abstraction.** The judgement call is explicit,
   scored, and revisitable — not a matter of taste.

## Exercises

1. Run the duplication report on one service. List every mapping that appears more than once
   and the number of copies.
2. Take the most-duplicated mapping and run the
   [abstraction cost analysis](./02-deep-dive/01-abstraction-cost-analysis.md). Write down the
   verdict and the three numbers that drove it.
3. Find one nested conditional chain in your error-handling code with **four or more branches**.
   Rewrite it as a decision table and count the lines before and after.
4. Measure the change cost of adding a new error code in your repo. If the answer is not
   "one file plus one registry row", list the extra edits and decide which one is removable.
5. Write a complexity budget for one feature (files, LOC, decision sites) and add the check to
   CI.

## Related

- [Chapter 54 — Reusable Error-Handling Infrastructure](../54-reusable-error-handling-infrastructure/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../../part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)
