# Chapter 39 — Partial Failures and Multi-Step Operations

> Part XV · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Chapter 23 — Transaction and Rollback Error Handling](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)

## One-sentence summary

A **partial failure** is a multi-step operation that stopped somewhere in the middle, and
production-grade handling means every such operation has **explicit intermediate states**, an
**ambiguity resolver**, and a **compensation path** that is safe to run twice.

## Why this chapter matters

Single-statement failures are easy: you get an error, you translate it, you respond. The damage
in distributed systems comes from operations that *partially* worked — the payment captured, the
inventory released, the email not sent. Because no single transaction spans the steps, the system
has no automatic way to be "all or nothing," so it ends up *somewhere*, and "somewhere" is
invisible unless you name it. This chapter is the difference between "the checkout failed" and
"the checkout is in state `COMPENSATING`, refund `rf_3k9` pending, retry in 30 s."

## Chapter map

The chapter has 16 sections grouped into nine files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-partial-failure-and-multi-step-operations.md`](./01-concepts/01-partial-failure-and-multi-step-operations.md) | 39.1–39.3 | What partial failure is, why multi-step ops create it, what happens after partial success |
| [`01-concepts/02-bulk-and-parallel-partial-success.md`](./01-concepts/02-bulk-and-parallel-partial-success.md) | 39.4, 39.5 | Per-item results in bulk work, aggregating parallel outcomes without lying |
| [`01-concepts/03-distributed-transactions-sagas-and-compensation.md`](./01-concepts/03-distributed-transactions-sagas-and-compensation.md) | 39.6–39.8 | Why 2PC blocks, what a saga is, how compensation fails |
| [`01-concepts/04-workflow-recovery-and-long-running-operations.md`](./01-concepts/04-workflow-recovery-and-long-running-operations.md) | 39.9–39.12 | Workflow recovery, long-running semantics, ambiguous completion, resuming interrupted work |
| [`01-concepts/05-states-compensation-safety-and-irreversibility.md`](./01-concepts/05-states-compensation-safety-and-irreversibility.md) | 39.13–39.16 | Explicit intermediate states, duplicate compensation, irreversible side effects, terminal vs recoverable |
| [`02-deep-dive/01-saga-and-compensation-mechanics.md`](./02-deep-dive/01-saga-and-compensation-mechanics.md) | 39.6–39.8, 39.14 (mechanics) | Orchestration vs choreography, compensation ledger, ordering, retrying a failed compensation |
| [`03-practical-examples/01-checkout-saga-with-compensating-actions.md`](./03-practical-examples/01-checkout-saga-with-compensating-actions.md) | 39.7, 39.8, 39.13–39.16 | A runnable Checkout saga: steps, ledger, compensations, failure injection |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Saga and partial-failure rules, anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Rollback vs compensation guide, state table, decision trees |

## Learning objectives

By the end you can:

- Point at any operation and name **where atomicity stops** and a sequence of steps begins.
- Enumerate the **intermediate states** of a workflow and say what each one promises a user.
- Distinguish a **local `ROLLBACK`** from a **compensation**, and pick compensation actions that
  are idempotent and ordered.
- Resolve an **ambiguous completion** (`unknown`) with a read-back instead of a blind retry.
- Design a **resumable** long-running operation with checkpoints that are safe under at-least-once
  re-execution.
- Recognize an **irreversible side effect** and move it to the end of the workflow.

## Key takeaways

1. **Partial failure is the default in a distributed system.** Any operation spanning two
   commit boundaries can stop between them; design for the middle, not just the ends.
2. **A saga is business-level undo, not transactional rollback.** It can fail, so compensation
   needs retries, its own error contract, and an operator-visible terminal state.
3. **`unknown` is a third outcome.** Timeout with an idempotency key and a read-back — never a
   guess in either direction.
4. **Explicit intermediate states are what makes recovery possible.** If the state is only in a
   local variable when the process dies, the workflow is lost.
5. **Order compensations in reverse dependency order**, and put irreversible effects last so the
   blast radius of a mid-workflow failure stays small.

## Exercises

1. Take your most important write path and draw it as steps; mark every point where the process
   could die. What state is the system in at each point?
2. For each step, write the compensation action. Which of them are not idempotent? Fix that.
3. Kill a worker mid-workflow in staging. Does the workflow resume, stall, or vanish?
4. Take one bulk operation and design its partial-success response shape (per-item status plus an
   aggregate). Show it to a frontend engineer and ask if they can act on it.
5. List every side effect in your system that cannot be undone (email sent, token issued, model
   called). Where do they sit in your workflows?

## Related

- [Chapter 40 — Consistency and Concurrency Failures](../40-consistency-and-concurrency-failures/README.md)
- [Chapter 41 — Process, Runtime, and Resource Failures](../41-process-runtime-and-resource-failures/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Glossary: partial failure, saga, compensation](../../GLOSSARY.md)
