# Chapter 52 — Failure-Path Analysis

> Part XX · _Estimated reading time: 100–130 min_
> **Prerequisite:** [Chapter 51 — Correctness Properties](../51-correctness-properties-of-error-handling/README.md), [Chapter 39 — Partial Failures and Multi-Step Operations](../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)

## One-sentence summary

Failure-path analysis is a **repeatable method** for finding the paths where your error handling
does not exist yet, mapping each one to a recovery policy, and proving that no cell was left empty.

## Why this chapter matters

Chapter 51 told you what "correct" means. This chapter is the *method* for getting there. It exists
because error handling fails in a predictable way: **the branches you did not write are the
branches that break**. Reviewers cannot see them, unit tests do not cover them, and the only
reliable way to find them is to enumerate them deliberately.

The method has five steps, and each one produces an artifact you can keep:

| Step | Artifact | Subsection |
| ---- | -------- | ----------- |
| 1. Identify failure points | Numbered list `FP-01…FP-nn` | 52.1 |
| 2. Enumerate failure modes | Matrix of point × mode | 52.2 |
| 3. Map modes → categories | Category column in the matrix | 52.3 |
| 4. Map categories → recovery | Policy column in the matrix | 52.4 |
| 5. Find the unhandled cells | Gap list with risk scores | 52.5 |

After that, five specialised passes cover the failure classes that step 1–5 tend to miss: nested
operations (52.6), multi-step workflows (52.7), dependency boundaries (52.8), concurrency (52.9),
shutdown and cancellation (52.10). Then the hard cases: failure during recovery (52.11) and
ambiguous outcomes (52.12). Finally, the prioritisation machinery: FMEA (52.13), the inventory
(52.14), and risk ranking (52.15).

The concepts folder teaches the method (52.1–52.8); the checkout example runs the whole method
end to end, including the five specialised passes and the two hard cases (52.1–52.12); and the
deep dive turns the result into a scored, owned backlog (52.13–52.15).

## Chapter map

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-enumerating-failure-points-and-modes.md`](./01-concepts/01-enumerating-failure-points-and-modes.md) | 52.1–52.2 | Where failures can occur, and the mode list for each point |
| [`01-concepts/02-mapping-modes-to-categories-and-recovery.md`](./01-concepts/02-mapping-modes-to-categories-and-recovery.md) | 52.3–52.4 | Turning modes into categories, and categories into policies |
| [`01-concepts/03-unhandled-nested-and-multi-step-paths.md`](./01-concepts/03-unhandled-nested-and-multi-step-paths.md) | 52.5–52.8 | Unhandled paths, nested calls, workflows, dependency boundaries |
| [`02-deep-dive/01-fmea-and-risk-prioritization.md`](./02-deep-dive/01-fmea-and-risk-prioritization.md) | 52.13–52.15 | FMEA scoring, the failure-mode inventory, risk ranking into a backlog |
| [`03-practical-examples/01-checkout-failure-path-analysis.md`](./03-practical-examples/01-checkout-failure-path-analysis.md) | 52.1–52.12 | The `Checkout` flow, analysed point by point, gap by gap |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Guide words, templates, scoring scales, risk matrix |

## Learning objectives

By the end you can:

1. Enumerate the failure points of a single operation in under 30 minutes, using a repeatable
   checklist rather than intuition.
2. Enumerate the **failure modes** at each point, including the ones nobody thinks about: wrong
   data, duplicate delivery, partial write, silent success.
3. Map every mode to an error category and every category to a recovery policy, and detect the
   **unhandled cells**.
4. Analyse the five hard classes: nested operations, multi-step workflows, dependency boundaries,
   concurrent interleavings, shutdown and cancellation.
5. Score failure modes with **FMEA** (severity × occurrence × detection = RPN) and turn the scores
   into a ranked backlog.
6. Maintain a **failure-mode inventory** that grows from incidents and stays aligned with the
   error registry and the test suite.

## Key takeaways

1. **The analysis must be finite.** One operation, a fixed mode list, a total mapping table. A
   whole-service analysis is a document nobody finishes.
2. **Unmapped cells are the deliverable.** The point of the analysis is not the matrix; it is the
   list of empty cells.
3. **Enumerate categories, not instances.** "Third-party API timeout" is one category with a
   policy; "Stripe 500 on Tuesday" is an incident, not a category.
4. **Ambiguity is a finding.** If you cannot say what happened, that is a gap — not a detail to
   resolve later.
5. **The inventory must live in the repo.** A spreadsheet decays; a file with a CI check survives.

## Exercises

1. Take `Checkout` (or your own flow) and enumerate 12 failure points in 30 minutes. Use the
   checklist in `01-concepts/01-enumerating-failure-points-and-modes.md`.
2. Build the mode × point matrix and count the empty cells after mapping categories and policies.
   That number is your backlog.
3. Score your top 10 rows with FMEA. Compute RPN. Explain the two rows where RPN disagrees with
   your instinct, and say which one you trust.
4. Add the top 5 rows to a failure-mode inventory file, and write the CI check that fails when a
   high-risk row has no owner.

## Related

- [Chapter 51 — Correctness Properties](../51-correctness-properties-of-error-handling/README.md)
- [Part XX index](../README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Glossary](../../GLOSSARY.md)
