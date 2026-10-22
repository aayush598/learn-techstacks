# Async Jobs, Partial Failure, and Specialized Categories (5.23, 5.24, 5.29, 5.30, 5.33–5.35)

> Part II · Chapter 5 · Sections 5.23, 5.24, 5.29, 5.30, 5.33–5.35 · _Estimated reading time: 30 min_
> **Prerequisite:** [Runtime, Resource, and Lifecycle Categories](./04-runtime-lifecycle-and-resources.md)

## In one sentence

This family covers **background jobs, scheduled tasks, partial completion, compensation, and the
specialized SaaS categories (AI/tools, webhooks, file upload)** — where the failure is *deferred*
and the hard problems are **duplicates, resumption, and terminal states**.

## Why this matters in production

Synchronous errors are visible; asynchronous ones are not. A job that "finished" but skipped half
its work, a webhook processed three times, an AI run that billed twice, an upload with orphaned
multipart parts — all silent until a customer notices. These categories live in Part XII and XVI,
but they must be **named in the taxonomy** so jobs, queues, and agents route correctly.

## 5.23 Background job

A **background job** is work deferred to a worker. Its lifecycle has explicit failure states:
`queued → running → (succeeded | failed | retrying | dead)`.

| Failure | Retry | Terminal? |
| ------- | ----- | --------- |
| transient (DB `40001`, `503`) | yes, backoff | no |
| permanent (validation, `422`) | no | **yes** — DLQ |
| exhausted attempts | no | **yes** — DLQ |
| poison message | no | **yes** — isolate |

Every job must declare **retryable vs terminal** (Chapter 32). A job that retries a permanent
failure forever is a **poison message** that blocks the queue.

## 5.24 Scheduled task

A **scheduled task** (cron) adds *time* as a dimension: it may **miss** a run (overlap, downtime),
**overlap** with a prior run, or run **late** during catch-up.

| Failure | Policy |
| ------- | ------ |
| missed while down | catch-up or skip (declare which) |
| overlapping runs | lock / singleton guard |
| long run past next tick | skip next or queue |
| failed run | alert; retry next tick or backoff |

Scheduled tasks need **idempotency** for the same reason jobs do: a scheduler that fires twice
must not double-process.

## 5.29 Partial completion

**Partial completion** means some steps/items succeeded and others did not. It is a *state*, not
just an error.

| Form | Example |
| ---- | ------- |
| multi-step op | charge succeeded, provision failed |
| batch | 990 of 1000 rows imported |
| parallel fan-out | 3 of 5 providers updated |

| Aspect | Value |
| ------ | ----- |
| HTTP | `500` or `207`-style detail for batch APIs |
| Retry | resume remaining, **never** redo completed work |
| Alert | depends on impact; data loss → page |

> ⚠️ **Hazard.** Marking a partially completed operation as fully "success" is silent corruption
> (Chapter 1). Represent partial state explicitly and record per-item results.

## 5.30 Compensation / rollback

**Compensation** logically undoes a completed step when a later step fails (refund, release
reservation, delete provisioned resource).

| Trigger | Compensation |
| ------- | ------------ |
| charge ok, provision failed | refund |
| reserve ok, payment failed | release reservation |
| publish ok, consumer reject | unpublish / tombstone |

Compensation itself can fail (Chapter 39.8); it must be **idempotent** and **retried** until
applied, and the overall flow must reach a terminal state (compensated / failed).

## 5.33 AI model / tool / token limit

LLM and tool-calling failures are their own category because they are **nondeterministic** and
have provider-specific limits (Chapter 44).

| Trigger | Signal | Policy |
| ------- | ------ | ------ |
| provider error | `5xx`, `429` | retry/ fallback model |
| rate/quota | `429` | backoff, degrade |
| token limit | `context_length_exceeded`, `finish_reason=length` | truncate/ summarize, no retry |
| invalid output | schema validation fails | re-ask or fail |
| tool failure | tool `5xx`/timeout | isolate tool, continue or abort |
| invalid tool args | validation | re-prompt, bounded |

| Aspect | Value |
| ------ | ----- |
| Retry | bounded; **non-idempotent side effects** need keys |
| Alert | warn (degrade), page only on total outage |
| Special | distinguish **provider** vs **app** errors |

## 5.34 Webhook delivery / processing

Webhooks are **at-least-once by nature** (Chapter 33): deliveries retry, duplicates happen, order
is not guaranteed.

| Failure | Handling |
| ------- | -------- |
| bad signature | `401`/`400`; never process |
| duplicate event | dedupe by event id — **idempotent** |
| out-of-order | reconcile by timestamp/version |
| slow processing | ack fast, process async |
| downstream failure | retry from provider; DLQ if exhausted |

Never 500 a webhook for a *permanent* reason (it will be redelivered forever, creating a poison
loop). Return a definitive status: `2xx` handled/ignored, `4xx` won't-come-back, `5xx` retry me.

## 5.35 File upload / processing / download

Files introduce their own category because of **size, format, and streaming** (Chapter 43).

| Stage | Failure | Policy |
| ----- | ------- | ------ |
| upload | too large (`413`), wrong type (`415`) | reject, permanent |
| upload | interrupted | resume/abort (multipart cleanup) |
| processing | malformed file | reject, quarantine |
| processing | malware | block, alert |
| processing | partial/transform fail | resume from checkpoint |
| download | temp URL expired | re-sign |
| download | stream aborted | cleanup |

Temp-URL expiry, orphaned multipart parts, and duplicate processing are the classic silent bugs
here.

## Worked example — ExportJob + WebhookIngest + AgentRun

```text
ExportJob:
  step 1 write S3 succeeded, step 2 index failed → 5.29 partial       → resume step 2, don't rewrite
  scheduled nightly run missed during deploy      → 5.24 scheduled     → catch-up (idempotent)
  3 attempts exhausted on bad row                 → 5.23 background_job→ DLQ, alert
WebhookIngest:
  same Stripe event delivered twice               → 5.34 webhook       → dedupe by event id
AgentRun:
  provider 429                                    → 5.33 ai_provider   → backoff/fallback model
  context_length_exceeded                         → 5.33 ai_token_limit→ summarize, no retry
```

## Key data / numbers

- Delivery guarantees (Chapter 33): at-least-once + idempotency ≈ effectively-once.
- Stripe webhook signature uses `Stripe-Signature` with a timestamp tolerance; reject stale
  timestamps to prevent replay.
- LLM `finish_reason=length` / `context_length_exceeded` = token limit (permanent, no retry).
- Multipart uploads must be **aborted** on failure or parts accrue storage cost.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` processed the same Stripe `invoice.paid` twice after a redelivery, creating
duplicate invoices. The category was `5.34 webhook` with a missing **dedupe key**. Adding
`event.id` dedupe plus idempotent handling made redelivery harmless. Separately, `ExportJob`
marked a partial run "complete"; the taxonomy now forces the `5.29 partial` outcome to record
per-item results.

## Trade-offs

| Category | Retry | Idempotency needed | Terminal state |
| -------- | ----- | ------------------ | -------------- |
| background_job | bounded | yes | DLQ |
| scheduled_task | next tick | yes | failed/skipped |
| partial | resume remainder | yes | partially_succeeded |
| compensation | until applied | yes | compensated |
| ai_provider | bounded | yes (side effects) | failed/degraded |
| webhook | provider-driven | **yes** | processed/ignored |
| file_processing | resume | yes | rejected/quarantined |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every job a terminal state | Retry permanent failures forever |
| Dedupe webhooks by event id | Trust single delivery |
| Record partial results per item | Mark partial as complete |
| Make compensation idempotent | Compensate twice |
| Treat token limits as permanent | Retry `context_length_exceeded` |

## Common mistakes

- **Poison loops** — 500-ing a webhook for a permanent reason.
- **Duplicate side effects** — no dedupe on replay.
- **Losing partial state** — restarting a batch from zero.
- **Non-idempotent compensation** — refunding twice.

## Checklist

- [ ] Does every job declare retryable vs terminal?
- [ ] Are webhooks deduped by event id?
- [ ] Is partial completion represented explicitly?
- [ ] Is compensation idempotent and retried to a terminal state?
- [ ] Are AI token limits and tool failures classified separately?

## Related

- [Runtime, Resource, and Lifecycle Categories](./04-runtime-lifecycle-and-resources.md)
- [Category Interactions and Overlaps](../02-deep-dive/01-category-interactions-and-overlaps.md)
- [Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [AI, LLM, and Tool-Calling Application Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
