# Part XV — Advanced Distributed-System Failure Handling

> **Chapters 39–41.** Everything before this part assumed you could see the failure. Part XV is
> about the failures you *cannot* see whole: a step succeeded on one node and died on the next,
> two writers raced, the process ran out of memory, the lease expired while the work was still
> running. These are the failures that produce wrong data instead of red error pages.

## Learning objectives

By the end of Part XV you will be able to:

1. Decompose any **multi-step operation** into steps with explicit intermediate states, and name
   the state the system is in after every possible interruption.
2. Choose between a **local transaction**, a **saga with compensation**, and a **two-phase commit**
   — and defend the choice with the failure modes it accepts.
3. Design **compensation** that is idempotent, ordered, and safe to retry, and know which side
   effects cannot be undone at all.
4. Diagnose and recover from **concurrency failures**: races, lost updates, version conflicts
   (`HTTP 409`), deadlocks (`SQLSTATE 40001` / `40P01`), lease expiry, and stale replicas.
5. Decide when a **process must terminate** rather than recover — and when recovery would be
   unsafe — covering uncaught exceptions, `unhandledRejection`, OOM, `EMFILE`, pool exhaustion,
   and failed shutdown.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 39 | [Partial Failures and Multi-Step Operations](./39-partial-failures-and-multi-step-operations/README.md) | Partial failure, sagas and compensation, long-running workflows, resumable state |
| 40 | [Consistency and Concurrency Failures](./40-consistency-and-concurrency-failures/README.md) | Races, optimistic locking, deadlocks, distributed leases, fencing, conflict resolution |
| 41 | [Process, Runtime, and Resource Failures](./41-process-runtime-and-resource-failures/README.md) | Uncaught errors, OOM, fd/socket/pool exhaustion, startup, shutdown, termination |

## How to study this part

- Read Chapter 39 first. **Partial failure is the root cause of most distributed bugs**; the other
  two chapters are specializations of it.
- For Chapter 40, implement the optimistic-locking example against your own hottest table before
  reading anything else — the failure only feels real once you reproduce `409` and `40001`.
- For Chapter 41, run one `SIGTERM` drill in staging: deploy, kill, and watch what your process
  does inside the grace period. Most teams discover their shutdown is not graceful only then.

## Key takeaways

- **Atomicity does not cross a network boundary.** A local ACID transaction ends where the
  connection ends; everything beyond it is a sequence of steps with an observable middle.
- **Compensation is not rollback.** A `ROLLBACK` restores bytes; a compensation performs a *new*
  business action (refund, release, re-open) that may itself fail, may be noticed by a customer,
  and may be impossible for irreversible side effects.
- **Ambiguity is a first-class outcome.** "The request timed out" is neither success nor failure —
  it is `unknown`, and every design must say how `unknown` is resolved.
- **Conflicts are normal, corruption is not.** `409`, `40001`, and `40P01` are the database
  telling you the truth about concurrency; the bug is converting them into lost updates.
- **Termination is a recovery mechanism.** Some states are only safe to fix by starting a fresh
  process — but only if shutdown is designed so that termination is itself safe.

## The recurring cast in this part

| Cast | Used here to teach |
| ---- | ------------------ |
| **Checkout** | Saga steps, compensation ordering, duplicate refunds, version conflicts on `carts` |
| **ExportJob** | Checkpoint/resume after a worker crash, partial bulk results, queue saturation |
| **WebhookIngest** | Concurrent duplicate events, unique-constraint races, stale replay |
| **AgentRun** | Multi-step tool calls with irreversible effects mid-run |
| **Acme SaaS** | The multi-tenant system all of the above live inside |

## Related

- [Part XIV — Frontend and Full-Stack Error Handling](../part-14-frontend-and-full-stack/README.md)
- [Part XVI — Specialized SaaS Error Scenarios](../part-16-specialized-saas-scenarios/README.md)
- [Glossary](../GLOSSARY.md)
- [Full table of contents](../_TOC.md)
