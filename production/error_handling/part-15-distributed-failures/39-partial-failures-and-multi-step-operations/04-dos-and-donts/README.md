# Chapter 39 — Do's and Don'ts

> Part XV · Chapter 39 · All sections

A condensed rule set distilled from the chapter. Use it as a review checklist before any
multi-step operation reaches production.

## Partial failure and multi-step operations (39.1–39.3)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enumerate every commit boundary before designing the flow | Assume "the whole service call" is one step |
| Persist progress (step ledger) with each step | Keep workflow progress in local variables |
| Distinguish partial **failure** from partial **success** in the contract | Report a designed per-item outcome as `500` |
| Give ambiguous outcomes a third state (`unknown`) | Collapse a timeout into success or failure |
| Return `202` + an id for work that outlives the request | Block a request until every step finishes |

## Bulk and parallel work (39.4–39.5)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return per-item status plus counts | Return one boolean for a 50,000-row batch |
| Derive aggregate status from item counts | Hand-set `status: "succeeded"` |
| Retry only the failed/unknown items | Re-run the whole batch on one failure |
| Use `allSettled`/errgroup for independent branches | Use `Promise.all` when every branch matters |
| Bound fan-out concurrency | Fan out to thousands of sockets at once |

## Sagas and compensation (39.6–39.8)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "can this store join a 2PC?" before proposing distributed transactions | Apply 2PC across Stripe/S3/the public internet |
| Orchestrate anything with money and >3 steps | Chase choreography events to find out if an order is paid |
| Make compensation idempotent by business key | Mint a new refund idempotency key per attempt |
| Retry compensation, then escalate to a human | `catch` a failed compensation and move on |
| Persist the compensate decision before undoing | Decide to undo only inside a `catch` block |

## Workflow recovery and long-running work (39.9–39.12)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every long workflow an expiry and a sweeper | Let `running` rows live forever |
| Resolve `unknown` by read-back before retrying | Guess "failed" and charge again |
| Claim a lease before resuming | Let two runners advance one workflow |
| Checkpoint data + offset in one transaction | Write the checkpoint after the data, separately |
| Report progress from the ledger | Report an in-memory counter |

## States, safety, and irreversibility (39.13–39.16)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model states as a closed enum | Use free-form status strings |
| Guard terminal transitions (`WHERE state=...`) | Set terminal state unconditionally |
| Keep `blocked` distinct from `failed` | Call an inconsistent system "failed, done" |
| Order steps reversible → costly → irreversible | Send the email before the payment settles |
| Record a transition history for support | Overwrite status with no history |

## Anti-patterns in the wild

1. **The Pretend Transaction** — `try/catch` around four independent commits; atomicity is
   cosmetic and partial failure is invisible.
2. **The Optimistic Refunder** — refunding on timeout before checking whether the charge exists.
3. **The Forever Loop** — a compensation retried infinitely with no alert; money stuck, nobody
   paged.
4. **The Amnesiac Runner** — resuming a workflow from memory after a crash, or resuming without a
   lease.
5. **The Boolean Batch** — one `success: false` for a batch where 97% worked.
6. **The Eager Notifier** — irreversible effects (email, webhook, LLM call) executed before the
   workflow is durably committed.
7. **The State String Drifter** — `"in-progress"`, `"in_progress"`, `"doing"` as three different
   states discovered during an incident.

## Chapter checklist

- [ ] Every multi-step flow names its commit boundaries and intermediate states.
- [ ] Every step has an idempotency key or an explicit "not idempotent, and here is why it is safe."
- [ ] Ambiguous outcomes have a documented read-back resolution.
- [ ] Compensation exists, is ordered, is idempotent, and escalates on exhaustion.
- [ ] Bulk APIs report per-item results; parallel work has a chosen aggregation policy.
- [ ] Long workflows are resumable, lease-guarded, and expiring.
- [ ] A crash-injection test covers each step boundary of the critical workflow.

## Related

- [Chapter 39 Reference](../05-reference/README.md)
- [Chapter 39 Index](../README.md)
- [Part XVII — Error Handling in Architecture and Code Organization](../../../part-17-organization/README.md)
