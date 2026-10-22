# Chapter 52 — Do's and Don'ts

> Part XX · Chapter 52 · All sections

A condensed rule set for running failure-path analysis and keeping the result alive.

## Enumerating failure points

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Number every failure point and keep the list in the repo | Describe the happy path and call it analysis |
| Include decision and interpretation points | Enumerate only writes and external calls |
| Walk the code in execution order | List libraries "that could fail" |
| Include the response boundary | Forget that writing the response can fail |
| Ask "what if it succeeded but we did not hear?" | Only consider "it failed" |
| Use guide words to generate modes | Rely on inspiration for the modes |
| Reuse the point list when policies change | Redo the enumeration from scratch each quarter |

## Mapping modes to categories and policies

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map every mode to exactly one category | Leave a mode with "it depends" |
| Split a mode by phase when the category differs | Pick one category arbitrarily |
| Treat an unclassifiable mode as a finding | Stop the analysis at an unknown |
| Make the category → policy mapping total | Leave a category without a policy |
| Make the mapping executable | Keep the mapping only in a document |
| Give every policy all six fields | Write "handle it" as a policy |

## Ambiguity and retries

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map an ambiguous outcome to *resolve later* | Map it to *transient* and retry |
| Read back by idempotency key before retrying | Retry blindly with a new key |
| Retry with the same idempotency key | Retry a charge because the response was slow |
| Treat "succeeded, response lost" as a first-class mode | Assume a timeout means nothing happened |
| Keep the retry budget under 10% of the deadline | Let retries own the request latency |
| Cap attempts at 5 with backoff and jitter | Loop until the call succeeds |

## Workflows and compensation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every irreversible effect a compensation row | Assume a later step will always succeed |
| Schedule compensation after the settlement window | Refund before the charge is known to have settled |
| Make compensation idempotent | Retry a refund from an unknown state |
| Order compensations so they cannot make things worse | Compensate in the order the steps ran |
| Keep the effects that must agree in one transaction | Write related rows in separate transactions |

## Concurrency, cancellation, and shutdown

| ✅ Do | ❌ Don't |
| ----- | -------- |
| State per effect: serialised, idempotent, or unsafe | Assume one worker per order |
| Run cancellation and shutdown as a pass over every effect | Treat a deploy as an exotic event |
| Make the post-kill state one the matrix already describes | Leave the mid-flight state undefined |
| Dedupe on the consumer side when the broker is at-least-once | Assume exactly-once delivery |
| Treat a client disconnect as a real mode | Assume the client is still waiting |

## Recovery failures

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write a policy for the recovery failing | Assume the recovery cannot fail |
| Queue an unavailable compensation and alert | Drop the compensation silently |
| Alert when reconciliation finds no record | Conclude "nothing happened" and return success |
| Terminate rather than continue on a failed rollback | Continue after a rollback failure |
| Never degrade into an error | Fall back to code that throws |

## Risk scoring and prioritisation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Score severity first | Let a noisy detection score inflate the ranking |
| Write down the evidence for each score | Split the difference in a disagreement |
| Use "5, unmeasured" for uninstrumented paths | Claim occurrence 1 for something you never measured |
| Treat RPN as a ranking, not a probability | Report RPN as a probability of failure |
| Give every row above the threshold an owner and a date | Leave high-RPN rows in an unowned backlog |
| Record accepted risks with a monitoring signal | Accept a risk and stop watching it |
| Re-score quarterly | Freeze the scores after the first analysis |

## Keeping the analysis alive

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the inventory in the repository | Keep it in a spreadsheet |
| Let incidents and analyses both create rows | Let incidents stay anecdotal |
| Check the inventory in CI | Rely on someone remembering to update it |
| Retire modes that no longer apply, with history | Delete rows and lose the reasoning |
| Version the matrix with the code it describes | Let the matrix drift from the code |
| Re-analyse a flow when its dependencies change | Re-analyse everything every quarter |

## Anti-patterns in the wild

- **The Happy-Path Matrix.** Ten rows that all say "works as expected" — a description of what
  should happen, not an analysis of what can.
- **Ambiguity Mapped to Transient.** The most expensive single decision in a matrix: it turns one
  lost charge into a retry storm of charges.
- **Effects Assumed Atomic.** Two writes that must agree, in two transactions, waiting for a
  concurrent request to find the gap.
- **The Response Forgotten.** Failing to *write* the response is a real failure point, and the
  one that makes clients retry.
- **Boundaries Trusted.** A `200` with an empty body is a mode, not a success.
- **The Category Wall.** Twelve categories and a twelve-branch `switch`, where the default
  branch handles 40% of the traffic.
- **Analysis Without a Backlog.** A matrix nobody scores produces a document, not a plan.
- **The Spreadsheet.** An inventory in a spreadsheet is a snapshot; in the repository it is a
  diff, reviewable in a pull request.
- **Severity Shopping.** Teams inflate severity to win the argument about priority.

## Quick self-check

Before you call an analysis done, answer these five questions:

1. **What is the blast radius?** How many customers, how much data, and how long until anyone
   notices?
2. **Which cells are empty?** The unhandled cells are the deliverable, not the matrix.
3. **Which modes are ambiguous?** Any mode where you cannot say whether the effect happened must
   resolve, never retry.
4. **What happens on a deploy?** Does every effect have a defined post-kill state?
5. **Who owns the top row?** An unowned row is not a backlog item.

## Related

- [Chapter 52 — Failure-Path Analysis](../README.md)
- [Failure-Path Analysis of the Checkout Flow](../03-practical-examples/01-checkout-failure-path-analysis.md)
- [FMEA, the Failure-Mode Inventory, and Risk Prioritization](../02-deep-dive/01-fmea-and-risk-prioritization.md)
- [Chapter 51 — Correctness Properties](../../51-correctness-properties-of-error-handling/README.md)
