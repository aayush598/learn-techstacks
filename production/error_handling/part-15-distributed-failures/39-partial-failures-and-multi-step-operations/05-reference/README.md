# Chapter 39 — Reference

> Part XV · Chapter 39 · Cheat sheets, rollback/compensation guide, and decision trees.

## Cheat sheet — partial failure outcomes

```text
step stops ─┬─ all steps committed ────────────────▶ succeeded
            ├─ earlier steps committed, N not ─────▶ partial → compensate
            ├─ N may or may not have committed ────▶ unknown  → read-back
            └─ ledger itself lost/gone ────────────▶ lost     → rebuild/escalate
```

| Outcome | HTTP | Client action |
|---------|------|---------------|
| Completed | `200` | none |
| Started, not finished | `202` + `Location`/id | poll status |
| In flight for same key | `409` | wait/poll, do not re-POST |
| Request invalid, nothing ran | `422` | fix input |
| Finished with item failures | `200` + `status: "partial"` + counts | retry listed items |
| Terminal, will not change | `410` | stop retrying |

## Rollback vs compensation guide

| Question | `ROLLBACK` | **Compensation** |
|----------|-----------|------------------|
| What is it? | Undo of uncommitted bytes inside one transaction | A *new* business action that logically undoes a committed step |
| When can it run? | Before/at commit failure | Only after a step is durably `done` |
| Scope | One database, one connection | Any number of services, providers, files |
| Failure mode | Rare (connection gone → server rolls back anyway) | Normal — retries, escalation required |
| Visibility | Invisible to users | Often visible (refund pending, released slot) |
| Cost | Free | Money (refund fees), time (days), reputation |
| Requires | a transaction | a ledger, idempotency keys, ordering, alerting |
| Never for | — | irreversible effects (email sent, token spent) |

**Rule:** if the effect left your transaction boundary, `ROLLBACK` is no longer available and you
are designing compensation — whether or not you called it that.

## Compensation design checklist

- [ ] Compensating action defined for every step with an external or money effect.
- [ ] Compensation runs in **reverse dependency order**.
- [ ] Idempotency: provider key (`refund:<saga_id>`) **and** ledger row (`step_key` PK).
- [ ] Read-back before create (list refunds / read state) to cover the crash window.
- [ ] Bounded retries (5–10 attempts, 15–30 min) then `blocked` + human alert.
- [ ] Irreversible steps excluded and positioned last.
- [ ] Sweeper resumes `compensating` rows whose lease expired.
- [ ] Terminal transition guarded: `UPDATE ... WHERE state='compensating'`.

## Decision tree — which structure?

```text
Does the operation stay inside ONE database with NO external calls?
├─ yes → single local transaction. Stop.
└─ no  → Can every participant vote in a 2PC you operate?
         ├─ yes, and blocking/lock-holding is acceptable → 2PC (rare)
         └─ no (Stripe/S3/queues/partners) → SAGA
              ├─ money, entitlements, >3 steps, user-visible state → ORCHESTRATION (durable FSM)
              └─ optional, low-stakes, event-shaped → CHOREOGRAPHY (+ a status read model)
```

## Decision tree — a step failed, now what?

```text
Is the outcome ambiguous (timeout / lost ack)?
├─ yes → read-back by idempotent marker
│        ├─ found      → treat as done, continue
│        ├─ not found + safe window → retry with the SAME key
│        └─ cannot tell → state 'unknown' / 'blocked' + alert. STOP.
└─ no  → is the error retryable AND the step idempotent?
         ├─ yes → retry step (bounded, jittered)
         └─ no  → persist state='compensating' → undo done steps in reverse
                  compensation retries exhausted → 'blocked' + page
```

## Saga state table

| State | Meaning | Auto-advanced by | Customer told |
|-------|---------|------------------|---------------|
| `pending` | created, not started | runner | `202 accepted` |
| `running` | executing steps | runner (lease) | `202 in progress` |
| `compensating` | undoing done steps | runner/sweeper | `202 being reversed` |
| `cancelling` | user/system requested stop | runner | `202 cancelling` |
| `blocked` | needs a human (ambiguous/compensation exhausted) | **nobody — alert** | `409 SAGA_BLOCKED` |
| `succeeded` | all steps done | — | `200` |
| `compensated` | fully undone | — | `200`/`410` |
| `cancelled` | stopped, no residual effects | — | `410` |
| `failed` | stopped, no residual effects, not retryable | — | `409`/`422` per code |
| `expired` | budget exceeded; partial effects compensated first | sweeper | `410` |

## Failure matrix — crash points

| Crash between | On resume |
|---------------|-----------|
| intent write and action | step `running`, no effect → re-run or resolve |
| action and outcome write | effect exists, ledger `running` → idempotent re-run / read-back |
| outcome write and outbox publish | outbox relay publishes on restart |
| failure recorded and compensate decision | **must** be recoverable — decision is durable |
| decision and first undo | sweeper sees `compensating`, continues |
| undo and ledger mark-done | provider idempotency key collapses the duplicate |

## Key numbers used in this chapter

| Item | Value |
|------|-------|
| Stripe `Idempotency-Key` replay window | 24 h |
| Response for started-but-unfinished work | `202 Accepted` |
| Response for in-flight duplicate / state conflict | `409 Conflict` |
| Response when nothing ran due to request problem | `422 Unprocessable Content` |
| Postgres deadlock detection (`deadlock_timeout`) | 1 s default → `40P01` |
| Serialization failure SQLSTATE | `40001` |
| MySQL lock wait default | 50 s (`innodb_lock_wait_timeout`) |
| Compensation escalation | 5–10 attempts over 15–30 min → `blocked` |
| Kubernetes `SIGTERM` grace period | 30 s default (`terminationGracePeriodSeconds`) |
| Outbox relay poll | 250 ms–2 s (sub-second with CDC) |

## Chapter glossary

| Term | Meaning |
|------|---------|
| Partial failure | Operation stopped after some steps committed |
| Partial success | Designed per-item outcome, reported per item |
| Ambiguous completion | Outcome unknowable to the caller; requires read-back |
| Saga | Sequence of local transactions with compensations |
| Compensation | Business-level undo of a committed step |
| Orchestration | One durable coordinator owns the workflow state |
| Choreography | Services advance the flow by reacting to events |
| Step ledger | Durable record of each step's state |
| Irreversible side effect | An effect with no undo (email, token spend) |
| Blocked | Inconsistent state requiring a human; not `failed` |
| Checkpoint | Durable boundary inside a long step for resume |
| Transactional outbox | Event row written with the state change, relayed after |

## Signposts

- Ambiguous commits in depth → [Ch. 23 (23.11–23.14)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/01-concepts/04-ambiguous-commits-and-idempotent-retries.md)
- Outbox mechanics → [Ch. 23 deep dive](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)
- Job lifecycle and DLQ → [Ch. 32](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- Leases and fencing tokens → [Ch. 40 (40.10–40.11)](../40-consistency-and-concurrency-failures/01-concepts/04-distributed-locks-fencing-and-replicas.md)

## Related

- [Chapter 39 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 39 Index](../README.md)
- [Part XV Index](../../README.md)
