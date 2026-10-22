# Partial Failure and Multi-Step Operations (39.1–39.3)

> Part XV · Chapter 39 · Sections 39.1–39.3 · _Estimated reading time: 20 min_
> **Prerequisite:** [Transaction Boundaries and Atomicity](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/01-concepts/01-transaction-boundaries-and-atomicity.md)

## In one sentence

A **partial failure** is a failure you can observe in the middle of an operation that was designed
to mean something only at the end — and it happens the moment your operation crosses **more than
one commit boundary**.

## Why this matters in production

Users do not experience "step 2 of 4 failed." They experience *money taken and no subscription*,
*CSV half-written*, *ticket created but assignee never notified*. Every one of those is a
multi-step operation that stopped after a success. Partial failures are the single largest source
of support tickets that begin with "but it said it worked," and the largest source of silent data
divergence between two services that each believe they are the source of truth.

## Core concept

```text
One commit boundary                 Two commit boundaries
┌──────────────┐                   ┌────────┐   ┌────────┐   ┌────────┐
│ BEGIN        │                   │ step 1 │──▶│ step 2 │──▶│ step 3 │
│ step 1       │                   └───┬────┘   └───┬────┘   └───┬────┘
│ step 2       │                       │ commit     │ commit     │ commit
│ COMMIT /     │                       ▼            ▼            ▼
│ ROLLBACK     │                    boundary     boundary     boundary
└──────────────┘                   ▲            ▲            ▲
atomic: no observable middle        └── a failure can stop HERE ──┘
```

| Term | Definition | Example |
| ---- | ---------- | ------- |
| **Multi-step operation** | A logical unit of work that spans two or more commit boundaries (DB txn, HTTP call, queue publish, file write). | Checkout: reserve inventory → charge card → create subscription → send receipt |
| **Partial failure** | The operation terminated after some steps committed and before others did. | Card charged, subscription row absent |
| **Partial success** | A *deliberate* outcome where some items/branches succeeded and others did not, reported per item. | 97 of 100 rows imported |
| **Ambiguous completion** | The operation may or may not have finished; the observer cannot tell. | Timeout after the charge |

The critical distinction: **partial failure is accidental and must be repaired; partial success is
designed and must be reported.** If your system cannot tell them apart, it will report the first
as the second.

## How it works (mechanics)

### 39.1 What is partial failure

A partial failure exists when three conditions hold:

1. The operation has **stated intent** ("place this order") that only makes sense as a whole.
2. It spans **more than one atomic unit** (two transactions, or a transaction plus a network call).
3. It can stop **between** those units — because of a crash, a timeout, a rejection, a deploy.

The set of points where it can stop is exactly the set of commit boundaries. Audit those first;
they are few and enumerable.

### 39.2 Multi-step operations

Decompose before you design. For each step, record:

| Property | Question | Why it matters |
| -------- | -------- | -------------- |
| Boundary | Which unit commits this step? | Defines where a stop is possible |
| Effect | Is it local (DB) or external (network, S3, Stripe)? | External effects need their own idempotency |
| Reversibility | Can it be undone, and how? | Determines compensation design |
| Order | Does any later step depend on it? | Determines compensation order |
| Observable? | Can a later process detect whether it ran? | Enables read-back resolution |

The usual Checkout decomposition:

```text
1. INSERT order (status='pending')        local, reversible (delete/void)
2. Reserve inventory                      local, reversible (release)
3. Charge card (Stripe)                   EXTERNAL, reversible via refund (costly)
4. UPDATE order (status='active')         local, reversible (cancel)
5. Publish `subscription.created` event   external-ish, idempotent via outbox
6. Send receipt email                     EXTERNAL, IRREVERSIBLE
```

Step 6 being irreversible is a *design input*: it goes last, and it runs only after the workflow
is durably `COMMITTED`.

### 39.3 Failure after partial success

When a step fails, exactly one of four things is true. Naming which is the whole job:

```text
                    ┌── every step committed ───────────▶ SUCCESS
                    │
step N fails ───────┼── N not committed, earlier ones are ─▶ PARTIAL FAILURE → compensate
                    │
                    ├── N may or may not have committed ─▶ AMBIGUOUS → resolve by read-back
                    │
                    └── the workflow record itself is gone─▶ LOST → rebuild from step ledger
```

Rules that follow from the diagram:

- **Never return "failed" while an earlier step is still committed.** That is the lie that creates
  charge-without-subscription.
- **Never return "failed" when the outcome is ambiguous.** Resolve it (`unknown` → read-back) or
  say `202 Accepted, status=pending`.
- **Write progress durably, not in memory.** A step ledger row committed with each step is what
  makes "earlier steps are committed" knowable after a crash.

## Worked example

```ts
// A multi-step operation without a ledger is undebuggable after a crash.
type StepState = "pending" | "done" | "compensated" | "failed";

async function runStep(wf: Workflow, step: Step, fn: () => Promise<void>) {
  // 1. Durably record intent BEFORE acting. This row is the source of truth.
  await db.query(
    `INSERT INTO workflow_steps (workflow_id, step, state)
     VALUES ($1, $2, 'pending') ON CONFLICT DO NOTHING`, [wf.id, step.name]);
  await db.query(
    `UPDATE workflow_steps SET state='running', attempt=attempt+1
     WHERE workflow_id=$1 AND step=$2 AND state IN ('pending','failed')`, [wf.id, step.name]);

  try {
    await fn();                                   // the actual effect (may be external)
    await db.query(
      `UPDATE workflow_steps SET state='done', done_at=now()
       WHERE workflow_id=$1 AND step=$2`, [wf.id, step.name]);
  } catch (err) {
    await db.query(
      `UPDATE workflow_steps SET state='failed', error_code=$3
       WHERE workflow_id=$1 AND step=$2`, [wf.id, step.name, classify(err).code]);
    throw new PartialFailure(wf.id, step.name, err);  // partial: earlier steps stay 'done'
  }
}
```

```text
Crash trace — process dies between step 3 and step 4:
  workflow_steps: reserve_inventory=done, charge=done, activate=pending
  reload on boot → resume engine sees 'done','done','pending'
  → decide: retry step 4 (idempotent by order_id) — no second charge, no lost order
```

## Key data / numbers

- A typical SaaS checkout has **4–7 commit boundaries**; each one is a place a partial failure can
  be born.
- Stripe's `Idempotency-Key` replays the original response for **24 hours** — the practical window
  for resolving an ambiguous charge by read-back.
- `HTTP 409 Conflict` is the correct response when a multi-step operation is already in flight for
  the same idempotency key; `422` is for validation; `202 Accepted` for "started, not finished."
- **Postgres has no cross-database transaction.** Two databases, two commits — always a partial
  failure window.
- Rule of thumb: a step ledger row should be committed **within the same transaction as the local
  effect** of that step, or immediately after an external one.

## Real-world use case — Acme SaaS

`Checkout` ran four steps inline in the HTTP request. A `pod` was rescheduled (deploy) right after
Stripe returned `201` and before the `subscriptions` insert. The customer had a paid plan in
Stripe and no plan in Acme — no entitlement, no invoice row, a silent outage for that tenant. The
fix was not "better try/catch": it was a **workflow row with a per-step ledger**, so on restart the
resume engine saw `charge=done` and completed `activate` instead of charging again. Support
tickets for "paid but locked out" dropped to zero over the following quarter.

## Trade-offs

| Approach | Pros | Cons | When to use |
| ----------|------|------|-------------|
| Single local transaction | Truly atomic, simplest | Cannot span services/Stripe/S3 | one database, no external effects |
| Steps + ledger + resume | Crash-safe, auditable, resumable | More tables, more states to own | any workflow with external effects |
| Steps with no ledger | Fewer moving parts | Undiagnosable after a crash | never for anything that costs money |
| Synchronous all-in-request | Simple UX | client timeout makes outcome ambiguous | only if all steps are fast and local |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enumerate commit boundaries before writing the workflow | Assume "the service call is one step" |
| Commit intent (ledger) before performing a step | Keep workflow state only in memory |
| Distinguish partial failure from partial success in the contract | Return `500` for a designed per-item outcome |
| Return `202`/`409` while a workflow is in flight | Block the request until every step finishes |
| Put irreversible steps last | Send the email before the payment settles |

## Common mistakes

- **Treating the workflow as the transaction** — a `try/catch` around four steps that each commit
  independently gives the *appearance* of atomicity and the reality of partial failure.
- **Logging progress instead of persisting it** — after a restart the log says what happened, not
  what is true now.
- **One error type for all four outcomes** — success, partial, ambiguous, and lost need distinct
  states, codes, and HTTP mappings.
- **Compensating on a failure that is still ambiguous** — you may refund a charge that never
  happened, or skip one that did.

## Checklist

- [ ] Every commit boundary in the critical path is listed in the design doc.
- [ ] Each step has: effect, reversibility, order dependency, detectability.
- [ ] Progress is durable and reloadable, not in-process.
- [ ] The API contract distinguishes success, partial, in-flight, and unknown.
- [ ] Irreversible steps run after the workflow is durably committed.
- [ ] A crash mid-workflow is a test you have actually run.

## Related

- [Bulk and Parallel Partial Success (39.4–39.5)](./02-bulk-and-parallel-partial-success.md)
- [Distributed Transactions, Sagas, and Compensation (39.6–39.8)](./03-distributed-transactions-sagas-and-compensation.md)
- [Workflow Recovery and Long-Running Operations (39.9–39.12)](./04-workflow-recovery-and-long-running-operations.md)
- [Ambiguous Commits and Idempotent Retries (23.11–23.14)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/01-concepts/04-ambiguous-commits-and-idempotent-retries.md)
