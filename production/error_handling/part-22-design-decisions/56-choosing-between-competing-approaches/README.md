# Chapter 56 — Choosing Between Competing Approaches

> Part XXII · _Estimated reading time: 120–150 min_
> **Prerequisite:** [Chapter 7 — Error Classes, Types, and Structured Results](../../part-03-error-models/07-error-classes-types-and-structured-results/README.md), [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)

## One-sentence summary

Error-handling design is a set of **paired alternatives** — throw or return, centralize or
localize, retry or compensate — and choosing well means you can **name the failure, the layer,
and the risk tier** that made one side of the pair correct.

## Why this chapter matters

Almost every design debate in error handling is a false binary that has already been settled
somewhere else in the industry. Teams burn weeks arguing "exceptions or results?" when the
real answer for a SaaS product is **both, in different layers** — and the decision that
actually matters is *which layer owns which*. They argue "global handler or local handling?"
when the real question is *where is the decision made, and where is the fallback owned?*.

The cost of getting this wrong is not aesthetic. It shows up as:

- A **duplicate payment** because a saga step retried instead of compensating.
- A **5xx on every request** because the global handler swallowed a per-tenant authorization
  failure and re-threw it as an internal error.
- A **cannot-reproduce incident** because a wrapper dropped the vendor request ID.
- A **rewrite** six months later because the chosen abstraction cost more than the bug it
  prevented.

This chapter gives you a **rubric**, not a preference list.

## Chapter map

The chapter has 18 subsections. They are grouped into four concept files, two deep dives, and
two worked examples:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-control-flow-shape.md`](./01-concepts/01-control-flow-shape.md) | 56.1, 56.7, 56.14 | Throw vs return, exceptions vs results, and collect-all vs first-error — how failure travels through code |
| [`01-concepts/02-structure-and-ownership.md`](./01-concepts/02-structure-and-ownership.md) | 56.2, 56.3, 56.9, 56.10, 56.11, 56.12 | Centralized vs local, global vs domain classes, generic vs specific, inheritance vs composition, universal vs bounded hierarchy, shared infra vs feature-owned |
| [`01-concepts/03-recovery-policy-tradeoffs.md`](./01-concepts/03-recovery-policy-tradeoffs.md) | 56.4, 56.5, 56.6, 56.15, 56.16 | Fail-fast vs degradation, retry vs immediate failure, retry vs compensation, sync vs deferred recovery, local recovery vs termination |
| [`01-concepts/04-fidelity-and-risk.md`](./01-concepts/04-fidelity-and-risk.md) | 56.8, 56.13, 56.17, 56.18 | Wrapping vs preserving, strict vs permissive, abstraction vs indirection, and policies selected by business risk |
| [`02-deep-dive/01-abstraction-vs-indirection-cost.md`](./02-deep-dive/01-abstraction-vs-indirection-cost.md) | 56.17, 56.2, 56.11, 56.12 | The cost model for indirection: when a shared layer pays for itself and when it is a tax |
| [`02-deep-dive/02-risk-based-policy-selection.md`](./02-deep-dive/02-risk-based-policy-selection.md) | 56.18, 56.4, 56.5, 56.6 | Turning business risk into concrete retry/fallback/termination policies |
| [`03-practical-examples/01-checkout-decision-walkthrough.md`](./03-practical-examples/01-checkout-decision-walkthrough.md) | 56.1–56.18 (applied) | A full decision walkthrough for the `Checkout` flow, from throw-vs-return to termination policy |
| [`03-practical-examples/02-exportjob-and-agentrun-selection-matrix.md`](./03-practical-examples/02-exportjob-and-agentrun-selection-matrix.md) | 56.1–56.18 (applied) | The same matrix applied to `ExportJob` and `AgentRun`, showing why the rubric generalizes but the answers do not |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | The rules that survive every debate, plus the anti-patterns behind each wrong answer |
| [`05-reference/README.md`](./05-reference/README.md) | all | The 18-pair decision matrix, the abstraction cost table, the risk-tier policy table |

## Learning objectives

By the end you can:

1. Given any of the 18 pairs, state the **question being asked**, the **two real answers**,
   and the **tie-breaker** that separates them.
2. Choose a control-flow shape (exception, result, or hybrid) for a specific module and justify
   it by its callers, not by its author.
3. Decide where a decision lives (registry, classifier, policy table) versus where a *fallback*
   lives (boundary), and defend the split.
4. Compute the cost of an abstraction layer — in code, in runtime, and in cognitive load — and
   say when it has paid for itself.
5. Produce a **risk-tiered policy** for a set of operations, so that an AI summary failure and
   a payment capture failure get different recovery.
6. Write a one-page decision record for a contested error-handling choice that a reviewer can
   challenge on the merits.

## The 18 pairs at a glance

| # | The pair | Default answer | Tie-breaker |
| - | ------- | -------------- | ----------- |
| 56.1 | Exceptions vs results | Both, by layer | Can the caller enumerate the failures? |
| 56.2 | Centralized vs local handling | Centralized *policy*, local *fallback* | Who owns the fallback? |
| 56.3 | Global vs domain error classes | Domain classes, global base | Does the error need domain vocabulary? |
| 56.4 | Fail-fast vs degradation | Depends on the tier of the operation | Is a degraded answer useful? |
| 56.5 | Retry vs immediate failure | Retry transient + idempotent only | Will the second attempt succeed? |
| 56.6 | Retry vs compensation | Retry only if the effect did not happen | Did the side effect already occur? |
| 56.7 | Throwing vs returning | Throw in the domain, return at the boundary | Is failure part of the contract? |
| 56.8 | Wrapping vs preserving | Preserve first, then add context | Can the original be reconstructed? |
| 56.9 | Generic vs specific | Specific, until it duplicates | How many call sites branch on it? |
| 56.10 | Inheritance vs composition | Composition by default | Will the hierarchy grow branches? |
| 56.11 | Universal vs bounded hierarchy | Bounded, per domain | Can two domains share a vocabulary? |
| 56.12 | Shared infra vs feature-owned | Feature-owned until 3 real consumers | Is the concept product-neutral? |
| 56.13 | Strict vs permissive | Strict at trust boundaries, permissive inside | Who owns the data? |
| 56.14 | Aggregation vs first-error | Aggregate for user input, first-error for steps | Is the caller obliged to know all failures? |
| 56.15 | Sync vs deferred recovery | Sync when the user waits; deferred otherwise | Is the caller waiting for the outcome? |
| 56.16 | Local recovery vs termination | Recover locally; terminate the process only when corrupt | Is continued execution safe? |
| 56.17 | Abstraction vs indirection | Abstraction when 3+ consumers share the concept | Does the layer hide a decision or move it? |
| 56.18 | Policies by business risk | Tier by blast radius and reversibility | What breaks if we get it wrong? |

## Key takeaways

1. **These are pairs, not winners.** Every entry above has a legitimate case on both sides.
   A design is wrong when it picks one side *unconditionally*.
2. **The tie-breaker is almost always about the caller or the owner.** "What can the caller
   enumerate?" beats "exceptions are cleaner", and "who owns the fallback?" beats
   "centralization reduces duplication".
3. **Centralize decisions; localize effects.** The registry, classifier, and policy tables
   should be shared. The catch blocks, fallbacks, and user messages should not.
4. **Preserving is a precondition for everything else.** Once you drop the cause, the vendor
   code, or the request ID, no amount of structural elegance helps the next engineer.
5. **Risk tiering is where policy meets business.** `Checkout` and `AgentRun` are both "an
   error"; they have opposite retry, fallback, and termination policies.
6. **Abstraction must be earned by evidence.** Three real consumers, one concept, and a
   measurable reduction in duplication — otherwise it is indirection you pay for forever.

## Exercises

1. Take the four highest-traffic endpoints in your service. For each, write the pair decisions
   (56.1, 56.4, 56.5, 56.15) in one sentence each, and name the tie-breaker you used.
2. Audit for **double handling**: find any error that is both translated at a boundary *and*
   re-classified further up. Count the duplicates. (Teams typically find 3–9 per service.)
3. Write a decision record for one contested choice in your codebase, using the template in
   [`05-reference/README.md`](./05-reference/README.md). Circulate it to two reviewers who
   disagree with you — that is how you find out whether the rubric is real.
4. Compute the **indirection cost** of your error-handling stack using the table in
   [`02-deep-dive/01-abstraction-vs-indirection-cost.md`](./02-deep-dive/01-abstraction-vs-indirection-cost.md).
   Which layer is closest to costing more than it saves?
5. Assign each of your top 20 error codes a **risk tier** (from
   [`01-concepts/04-fidelity-and-risk.md`](./01-concepts/04-fidelity-and-risk.md)). Any code
   you cannot tier is a code whose policy is accidental.

## Related

- [Chapter 57 — Error Handling Under Load and at Scale](../57-error-handling-under-load-and-at-scale/README.md)
- [Part XXII index](../README.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
- [Glossary](../../GLOSSARY.md)
