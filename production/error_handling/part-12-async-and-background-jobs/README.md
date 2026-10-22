# Part XII — Asynchronous Processing and Background Jobs

> **Chapters 31–33.** Once work leaves the request/response cycle, failure handling changes shape.
> There is no user waiting to see an error, no stack trace returned to a caller, and no guarantee
> that a job runs exactly once. This part teaches you how to detect, contain, retry, and terminate
> failures in async code, queue workers, scheduled tasks, events, and webhooks.

## Learning objectives

By the end of Part XII you will be able to:

1. Reason about **error propagation across async boundaries** — promises, callbacks, streams,
   reactive pipelines, and event emitters — and prevent detached failures.
2. Design **background job failure policies**: retryable vs terminal, backoff, max attempts, poison
   messages, dead-letter queues, checkpointing, and safe replay.
3. Build **reliable event and webhook consumers** using signatures, idempotency, ack/reject
   semantics, ordering rules, and partial-batch failure reporting.
4. Write a **standard job error contract** that carries enough context to retry, alert, and replay
   without guesswork.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 31 | [Asynchronous Error Handling](./31-asynchronous-error-handling/README.md) | Sync vs async semantics, unhandled rejections, concurrent failure aggregation, cancellation, streams, cleanup |
| 32 | [Background Jobs, Queues, and Scheduled Tasks](./32-background-jobs-queues-and-scheduled-tasks/README.md) | Job lifecycle, retries, backoff, poison messages, DLQs, worker crashes, checkpointing, replay |
| 33 | [Events, Webhooks, and Message Processing](./33-events-webhooks-and-message-processing/README.md) | Publish/consume failures, delivery guarantees, duplicates, ordering, signatures, schema versions, eventual consistency |

## How the chapters fit together

```text
   request thread                  background plane
  ┌────────────────┐   enqueue    ┌─────────────────────────────────────┐
  │  API handler   │ ───────────▶ │ Job worker  (Ch. 32)                │
  │  returns 202   │              │  retry → backoff → DLQ → replay      │
  └────────────────┘              └─────────────────────────────────────┘
           │                                    ▲
           │ publish event                      │ consume
           ▼                                    │
  ┌────────────────┐                    ┌────────────────────────────────┐
  │ Event bus /    │ ─────────────────▶ │ Event consumer (Ch. 33)        │
  │ webhook source │                    │  verify → dedupe → ack/reject  │
  └────────────────┘                    └────────────────────────────────┘
           ▲
           │ all of the above run on async primitives (Ch. 31)
```

- **Chapter 31** is the substrate: if you cannot propagate and aggregate async errors correctly,
  your worker and consumer policies will leak failures.
- **Chapter 32** is the job plane: durable units of work with explicit lifecycle states.
- **Chapter 33** is the message plane: events and webhooks, where delivery guarantees and
  duplicates are the default assumption.

## The recurring cast in this part

| Cast member | Role in Part XII |
| ----------- | ---------------- |
| **ExportJob** | Long-running CSV/S3 export: checkpointing, resume, DLQ, idempotent object keys |
| **WebhookIngest** | Inbound Stripe webhooks: signature verification, dedupe, retries, replay |
| **AgentRun** | Background LLM tool-calling: parallel tool calls, cancellation, partial success |
| **Checkout** | Payment workflow whose async steps must never double-charge |
| **Acme SaaS** | Multi-tenant platform running all of the above on SQS/Redis workers |

## Key takeaways

- **Async failures do not propagate the way sync failures do.** A rejected promise with no handler
  becomes an unhandled rejection, not a thrown exception at the call site.
- **Concurrency is a policy decision.** `Promise.all` (fail-fast) and `Promise.allSettled`
  (collect-all) answer different product questions; pick deliberately.
- **At-least-once is the default reality.** Exactly-once is a property you *build* with idempotency,
  not a property most transports *give* you.
- **A dead-letter queue is not a graveyard.** It is a quarantine with a replay procedure, an owner,
  and an alarm.
- **Every job and event needs a terminal state.** Infinite retries are an outage that never pages.

## Exercises

1. Take one async function in your codebase and trace every path where its promise can reject
   without an attached handler. Attach an owner to each path.
2. List every background job you run. For each, write its retryable errors, max attempts, and what
   happens on exhaustion.
3. Pick one inbound webhook. Verify its signature header, define its duplicate key, and write the
   replay procedure for its DLQ.
4. Draft a job error contract (fields, codes, context) and apply it to two different jobs.

## Related

- [Part XI — Retry Logic and Resilience](../part-11-retry-and-resilience/README.md)
- [Chapter 33 — Webhook and Event Security](./33-events-webhooks-and-message-processing/01-concepts/04-webhook-signatures-retries-timeouts.md)
- [Chapter 32 — Poison Messages and Dead-Letter Queues](./32-background-jobs-queues-and-scheduled-tasks/01-concepts/03-poison-messages-dlq-and-replay.md)
- [Glossary](../GLOSSARY.md)
