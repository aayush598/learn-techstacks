# Part XXII — Advanced Error-Handling Design Decisions

> **Chapters 56–57.** You now have a taxonomy, an error model, boundaries, resilience
> mechanisms, and an organizational layout. Two questions remain, and they are the ones that
> separate a working design from a *defensible* one: **which competing approach do I pick, and
> does my design survive load?**
>
> Part XXII answers both with decision rules rather than preferences.

## Learning objectives

By the end of Part XXII you will be able to:

1. **Choose deliberately** between the 18 recurring error-handling alternatives (exceptions vs
   results, centralized vs local, retry vs compensation, wrapping vs preserving, …) using a
   consistent rubric instead of habit.
2. **Tier policies by business risk** — a failed AI summary and a failed payment capture do not
   deserve the same retry, fallback, or termination policy, even though both raise the same
   `Error` type.
3. **Predict amplification** — compute how many upstream calls a single downstream failure
   produces, and prove that your retry budget, bulkheads, and queue bounds keep the storm from
   becoming an outage.
4. **Isolate** tenants, features, and dependencies so that one noisy workload cannot exhaust
   shared resources for everyone.
5. **Stay correct when you scale horizontally** — same policy on every instance, no shared
   mutable state in the error path.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 56 | [Choosing Between Competing Approaches](./56-choosing-between-competing-approaches/README.md) | Control-flow shape, structure and ownership, recovery policy, fidelity vs risk, and the cost of abstraction |
| 57 | [Error Handling Under Load and at Scale](./57-error-handling-under-load-and-at-scale/README.md) | Error storms, failure amplification, isolation, bounding queues and retries, backpressure, and multi-instance consistency |

## How to study this part

- **Chapter 56 is a rubric.** Every file in it ends with a decision table. Read the tables
  first, then audit one real codebase (`Checkout` is the worked example) against them.
- **Chapter 57 is arithmetic.** The deep dives are full of formulas: amplification factor,
  retry budget, queue drain time, error-budget burn rate. Plug *your* numbers in — a policy
  you cannot compute is a policy you cannot defend in an incident review.
- **Both chapters are pairs.** Chapter 56 picks the policy; Chapter 57 checks whether the
  policy still holds when load multiplies everything by 100.

## Key takeaways

- **Every competing approach is right somewhere.** The question is never "which is better" but
  **"for which failure, in which layer, under which risk tier"**. A result type in the domain
  and an exception at the transport boundary is not a contradiction — it is a design.
- **Centralize decisions, not handling.** A single registry, classifier, and policy table beat
  a global `catch` block; a global `catch` block beats nothing, but loses context.
- **Preserve before you improve.** Wrapping that drops `cause`, vendor code, or request ID
  converts a diagnosable failure into a mystery. Add context; never replace the cause.
- **Under load, errors are load.** Each error costs CPU (stack capture), memory (allocation),
  and downstream attempts. Three hundred `500`s can be the *cause* of a latency spike, not its
  symptom.
- **Amplification is the mechanism of outages.** A 10% dependency error rate with 3 retries
  and 2 call layers can produce 90%+ extra downstream load. Bounding retries is not
  politeness; it is capacity planning.
- **Isolation beats redundancy.** Two instances sharing one connection pool is one instance
  with extra steps. Bulkheads, per-tenant limits, and separate pools are what make
  horizontal scaling actually multiply capacity.

## Related

- [Part XXI — Error Handling for Maintainability](../part-21-maintainability/README.md)
- [Part XXIII — Special Cases and Frequently Overlooked Failure Modes](../part-23-special-cases/README.md)
- [Glossary](../../GLOSSARY.md)
