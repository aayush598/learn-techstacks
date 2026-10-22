# Chapter 32 — Background Jobs, Queues, and Scheduled Tasks

> Part XII · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 31 — Asynchronous Error Handling](../31-asynchronous-error-handling/README.md)

## One-sentence summary

A background job is a **durable unit of work with an explicit lifecycle**, and production-grade job
handling means every job ends in a known state — `succeeded`, `failed`, `cancelled`, or quarantined
in a dead-letter queue — with enough context to retry, alert, and replay it.

## Why this chapter matters

Background work is where failures go to hide. The API returned `202`, the user moved on, and the
worker crashed at 3 a.m. Without lifecycle states, retry policy, and a DLQ, the failure is a silent
gap: invoices not generated, exports never delivered, tenants quietly churning. Queues also change
the failure model — **at-least-once delivery is the norm**, so a worker crash can run the same job
twice. This chapter teaches the policies and mechanics that make those failures bounded and visible.

## Chapter map

The chapter has 22 sections grouped into twelve files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-job-lifecycle-and-failure-states.md`](./01-concepts/01-job-lifecycle-and-failure-states.md) | 32.1–32.3, 32.9, 32.18 | Lifecycle, job boundary, retryable vs terminal, failed state, scheduled tasks |
| [`01-concepts/02-retries-backoff-and-exhaustion.md`](./01-concepts/02-retries-backoff-and-exhaustion.md) | 32.4–32.6, 32.21 | Delayed retries, backoff, max attempts, permanent vs exhaustion |
| [`01-concepts/03-poison-messages-dlq-and-replay.md`](./01-concepts/03-poison-messages-dlq-and-replay.md) | 32.7, 32.8, 32.17 | Poison messages, DLQ design, safe replay |
| [`01-concepts/04-worker-failures-timeouts-and-isolation.md`](./01-concepts/04-worker-failures-timeouts-and-isolation.md) | 32.10–32.13, 32.19 | Timeout/cancel, crashes, shutdown, duplicate delivery, isolation |
| [`01-concepts/05-partial-completion-and-failure-contracts.md`](./01-concepts/05-partial-completion-and-failure-contracts.md) | 32.14–32.16, 32.20, 32.22 | Partial completion, checkpointing, compensation, context, error contract |
| [`02-deep-dive/01-poison-message-handling.md`](./02-deep-dive/01-poison-message-handling.md) | 32.7–32.9, 32.17 (mechanics) | Visibility timeout, receive counts, redrive policy, replay safety |
| [`02-deep-dive/02-at-least-once-vs-exactly-once.md`](./02-deep-dive/02-at-least-once-vs-exactly-once.md) | 32.13 (mechanics) | Delivery guarantees and idempotent job design |
| [`02-deep-dive/03-checkpointing-and-idempotent-resume.md`](./02-deep-dive/03-checkpointing-and-idempotent-resume.md) | 32.14–32.15 (mechanics) | Durable checkpoints, resume semantics, at-least-once resume |
| [`03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md`](./03-practical-examples/01-exportjob-worker-with-dlq-and-backoff.md) | 32.4–32.8, 32.22 | A complete ExportJob worker with retries, backoff, and DLQ |
| [`03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md`](./03-practical-examples/02-scheduled-tasks-and-graceful-shutdown.md) | 32.12, 32.18, 32.19 | Cron overlap, shutdown draining, isolation |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Job rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Failure policy, job error contract, decision tables |

## Learning objectives

By the end you can:

- Draw the **job lifecycle** and name every terminal state.
- Classify an error as **retryable vs terminal** and configure attempts, delay, and backoff.
- Recognize a **poison message** before it stalls a queue and route it to a DLQ.
- Make a job **idempotent and resumable** under at-least-once delivery.
- Write a **standard job error contract** that preserves failure context.
- Drain workers safely on `SIGTERM` without losing or duplicating work.

## Key takeaways

1. **A job without a terminal state is a leak.** Every path must end in success, failure,
   cancellation, or quarantine.
2. **Retries are loans against idempotency.** Retry only classified-transient errors, and only if
   re-execution is safe.
3. **Poison messages must be evicted by count, not by hope.** `maxReceiveCount` + DLQ is the
   mechanism; replay is the recovery.
4. **Checkpointing turns a long job into resumable segments**, but resume is at-least-once too.
5. **Failure context is part of the job.** If the DLQ record lacks tenant, input, and attempt
   history, replay is guesswork.

## Exercises

1. List every job type you run and fill in: trigger, timeout, max attempts, retryable codes, DLQ.
2. Deliberately send a malformed job payload and verify it lands in the DLQ rather than looping.
3. Kill a worker with `SIGKILL` mid-job and confirm the message is redelivered and the job is
   idempotent.
4. Write a replay runbook for one DLQ, including who approves and how duplicates are avoided.
5. Define the job error contract for two different jobs and diff them for shared fields.

## Related

- [Chapter 31 — Asynchronous Error Handling](../31-asynchronous-error-handling/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../33-events-webhooks-and-message-processing/README.md)
- [Chapter 27 — Retry Policies](../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 28 — Idempotency](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../GLOSSARY.md)
