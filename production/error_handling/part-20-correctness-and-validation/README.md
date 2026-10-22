# Part XX — Error-Handling Correctness and Validation

> **Chapters 51–52.** Every previous part told you how to *design* error handling. This part asks
> the harder question: **how do you know it is correct?** Not "it compiles", not "we have
> try/catch", but: can you prove that every failure path ends somewhere defined, leaks nothing,
> terminates, cleans up, and tells the truth?

## Why this part exists

Most error-handling code is written once and never audited. It looks fine because the happy path
passes tests. The defects live in the branches nobody exercises: the timeout after the charge, the
`catch` that returns `null`, the retry loop with no ceiling, the compensation that runs twice.

Two practices close that gap:

1. **Correctness properties** — a fixed, checkable list of statements that must be true of *every*
   failure path, independent of which feature you are building.
2. **Failure-path analysis** — a systematic method for finding the paths in the first place, before
   a customer finds them for you.

Properties without analysis are aspirational. Analysis without properties produces a long list of
failures with no pass/fail criterion. You need both.

## Learning objectives

By the end of Part XX you will be able to:

1. State and apply the **18 correctness properties** of production error handling to a real
   service, and produce evidence for each (test, invariant, or code mechanism).
2. Build a **failure-path matrix** for a workflow: enumerate failure points, enumerate modes, map
   each to a category and a recovery policy, and identify the unhandled cells.
3. Run a **FMEA** on an operation, score severity, occurrence, and detection, compute **RPN**, and
   turn the result into a ranked, owned backlog.
4. Maintain a **failure-mode inventory** that stays aligned with the error registry, the tests, and
   production incidents.
5. Audit a pull request for correctness properties without re-deriving the whole design.

## Chapters

| # | Chapter | Focus | Files |
| - | ------- | ----- | ----- |
| 51 | [Correctness Properties of Error Handling](./51-correctness-properties-of-error-handling/README.md) | The 18 properties, how to verify them, how to enforce them structurally | 2 deep-dives, 2 worked audits |
| 52 | [Failure-Path Analysis](./52-failure-path-analysis/README.md) | Finding failure points and modes, mapping to policy, FMEA, inventory, prioritization | 3 deep-dives, 2 worked analyses |

## The 18 properties at a glance

Grouped the way Chapter 51 teaches them. Each row is a testable claim, not a slogan.

| Group | Property | One-line test |
| ----- | -------- | ------------- |
| Determinism & completeness | 51.1 Defined outcome per failure path | Does every path reach a declared terminal state? |
| | 51.2 Never silently discarded | Does every caught error propagate, translate, or get recorded? |
| | 51.3 Deterministic classification | Same error ⇒ same code, category, retryability — always? |
| | 51.4 Causes recoverable | Can an operator reconstruct what happened from the error alone? |
| Safety & resources | 51.5 No sensitive exposure | Is every outbound error a projection through an allowlist? |
| | 51.6 Retries terminate | Is there a hard bound on attempts *and* elapsed time? |
| | 51.7 Cleanup occurs | Is every acquired resource released on every exit path? |
| | 51.8 Consistency preserved | Do invariants hold in the post-failure state? |
| | 51.9 No duplicate side effects | Does N-times delivery produce at most one effect? |
| Contracts & transformation | 51.10 Responses follow contracts | Does every emitted error validate against the schema? |
| | 51.11 Safe fallback for unknown | Does the default branch fail safe, never to success? |
| | 51.12 No unbounded recursion | Are retry, fallback, translation, and cause chains bounded? |
| | 51.17 Transformations preserve metadata | Does translation keep code, cause, retryability, context? |
| | 51.18 Predictable during dependency failures | Is behavior a function of dependency state, not timing? |
| Concurrency & partiality | 51.13 Concurrency-safe | Do N concurrent duplicates produce ≤ 1 effect? |
| | 51.14 Partial failures accurate | Do reported successes + failures equal attempted items? |
| | 51.15 Cancellation not success | Does a cancelled operation ever report success? |
| | 51.16 Recovery preconditions | Does recovery run only when its preconditions hold? |

## The analysis loop

```text
   ┌──────────────────────────── one operation ────────────────────────────┐
   │                                                                        │
   ▼                                                                        │
 enumerate           enumerate          map modes →      map category →    │
 failure points ───▶ failure modes ───▶ categories ───▶ recovery policy ───┤
 (52.1)              (52.2)             (52.3)            (52.4)            │
   │                                                                        │
   │             find unhandled cells (52.5) ──▶ score risk (52.13–52.15)   │
   │                        │                                               │
   └────────────────────────┴──▶ inventory row + test + owner ─────────────┘
```

Run this loop on **one operation at a time** — Checkout, `ExportJob`, `WebhookIngest`, `AgentRun`.
A whole-system analysis produces a document nobody finishes. One operation produces a matrix you
can actually close.

## Key data used throughout

| Quantity | Value used in examples | Why it matters |
| -------- | ---------------------- | -------------- |
| Risk score | severity (1–5) × likelihood (1–5) | Cheap ranking; 25 = act now |
| RPN | severity × occurrence × detection (each 1–10) | Adds "can we see it?" to the ranking |
| Action threshold | RPN ≥ 200 needs an action; ≥ 400 blocks release | Recommendation, tune per team |
| SLO 99.9% | 43.2 min of downtime per 30-day month | One 20-min incident burns 46% of budget |
| SLO 99.95% | 21.6 min per 30-day month | Financial paths usually live here |
| Retry ceiling | 3–5 attempts, total deadline < caller deadline | Prevents amplification |
| Retry budget | ≤ 10% of request volume | Prevents retry storms |
| Dedupe window | 24 h (payments), 30 d (webhooks) | Matches vendor replay windows |

## How to study this part

- Read Chapter 51 first. Do not skip the reference checklist — print it.
- Then read Chapter 52 and run the analysis on **your own** checkout or signup flow.
- Score at least the ten highest-impact rows with FMEA. You do not need all of them.
- Add one inventory row per incident retro. The inventory grows from reality, not from a workshop.

## Key takeaways

1. **Correctness is a property of paths, not of the happy path.** A feature is only as correct as
   its least-defined failure branch.
2. **Every property needs evidence.** "We handle errors" is not evidence; a test, an invariant
   query, or a structural mechanism is.
3. **The dangerous failures are silent and partial**, not loud ones. Rank them first.
4. **Analysis is finite.** One operation, a fixed mode list, a total mapping table. If your analysis
   has no end, it has no result.

## Exercises

1. Take the last three production incidents. For each, name the property (51.1–51.18) that was
   violated. Most incidents violate two.
2. Draw the Checkout flow from memory and mark every point where it can stop. Compare with
   [the worked analysis](./52-failure-path-analysis/03-practical-examples/01-checkout-failure-path-analysis.md).
3. Pick one service and compute its failure-path coverage: handled cells ÷ enumerated cells.
4. Write the first five rows of a failure-mode inventory for a feature you own.

## Related

- [Chapter 51 — Correctness Properties](./51-correctness-properties-of-error-handling/README.md)
- [Chapter 52 — Failure-Path Analysis](./52-failure-path-analysis/README.md)
- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- [Master index](../README.md) · [Glossary](../GLOSSARY.md)
