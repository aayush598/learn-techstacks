# `WebhookIngest`: One Failure Through the Whole Lifecycle

> Part IV · Chapter 11 · All sections 11.1–11.17 · _Estimated reading time: 26 min_
> **Prerequisite:** [The Lifecycle: Origin Through Classification](../01-concepts/01-lifecycle-overview.md)

## In one sentence

A single Stripe `invoice.payment_failed` webhook whose processing hits a **transient database
failure** — traced stage by stage from origin to terminal state, showing the owner, the
artifact, and the output of every lifecycle stage.

## Why this matters in production

Reading the lifecycle in the abstract is easy; recognizing it in *your* traces is the skill.
This file is a worked specimen: keep it next to your own webhook consumer and ask, for each
stage, "where is this in my code? what is my artifact?" Gaps found here cost an hour; gaps found
during an incident cost a day.

## The event and the failure

```text
 Stripe  ──POST /webhooks/stripe──▶  Acme WebhookIngest
 event: invoice.payment_failed (invoice_id=in_1QxY..., attempt #2 of Stripe's retries)
 failure: the consumer's DB write hits a connection reset (pool exhausted) mid-processing
```

## Stage-by-stage trace

**Stage 1 — Origin (11.1).** Class: *persistence/dependency*. The pool exhausted while the
consumer wrote the invoice-state row. Owner: infrastructure layer (Ch. 9, 9.7). Artifact so far:
a driver error object.

**Stage 2 — Detect (11.2).** The repository's query throws; the repo's translation point catches
it *immediately* — detection and stage 3 happen together at the boundary:

```ts
// repo/invoice-repo.ts
try { await tx.none(SQL_UPSERT_INVOICE_STATE, params); }
catch (err) {
  if (isPoolExhausted(err) || isConnectionReset(err))
    throw { code: "DB_UNAVAILABLE", retryable: true, cause: err };
  throw { code: "DB_WRITE_FAILED", retryable: false, cause: err };
}
```

**Stage 3 — Represent (11.3).** The standard `AppError` shape with stable code — the driver
object is now `cause`, nothing else travels.

**Stage 4 — Classify (11.4).** Registry lookup: `DB_UNAVAILABLE` → category `infrastructure`,
`retryable: true`, severity `operational`, `public: false`. Classification happened once, at
registration time; the error merely *carries* it.

**Stage 5 — Enrich (11.5).** The webhook application service attaches allowlisted context:

```ts
throw e.withContext({
  operation: "webhooks.stripe.invoice.payment_failed",
  tenantId: inv.customer.metadata.acmeTenant,
  resourceType: "invoice", resourceId: inv.id,
  stripeEventId: event.id,
});
```

**Stage 6 — Preserve cause (11.6).** Chain intact:
`DB_UNAVAILABLE` → repo error → `NetworkingError` (driver). Full chain goes to logs; nothing
public.

**Stage 7 — Propagate (11.7).** The error leaves the repository, crosses the application service
(untouched — it has no decision for *this* code yet... wait: the application service *is* the
decider; see stage 9), and arrives at the webhook boundary.

**Stage 8 — Translate (11.8).** Boundary translation for the HTTP response: the code maps to
status `503` via the shared table (Ch. 10 artifact). Translation preserved `retryable` and the
correlation ID.

**Stage 9 — Decide (11.9).** The webhook application service — the one decider — reads
classification + attempt context:

| Input | Value | Effect |
| ----- | ----- | ------ |
| `retryable` | `true` | candidate for retry |
| Stripe redelivery | yes (up to ~3 days of backoff) | **do not** retry long; return failure and let Stripe redeliver *or* consume internally once |
| decision | `RETRY-THROUGH-PRODUCER` | render `503`; Stripe redelivers |

This decision is webhook-specific policy that a global handler could never make safely
(Ch. 10, 10.10): "who retries" is a business/operational choice with exactly one right owner.

**Stage 10 — Apply (11.10).** In this design, no internal retry loop runs — the *applied* action
is the render that triggers Stripe's retry. (If the consumer owned retries, this stage would run
the bounded attempts; the `ExportJob` example next file shows that variant.) Budgets: Stripe's
redelivery schedule is the external budget; our side adds an **event-level dedupe** so the same
`event.id` processed twice is a no-op (idempotency, Ch. 28).

**Stage 11 — Render (11.11).** One writer (the filter, after `headersSent` check):

```json
{ "type": "https://acme.example/errors/DB_UNAVAILABLE",
  "title": "Service temporarily unavailable",
  "status": 503,
  "code": "DB_UNAVAILABLE",
  "request-id": "corr_5b8e0d" }
```

**Stage 12 — Finalize (11.12).** Before responding, the consumer records the event attempt:
`webhook_events(event_id, state='retry_pending_producer', code, correlation_id, attempts=1)` —
an idempotent upsert keyed on `event_id`. Even if the process dies next, the record exists.

**Stage 13 — Cleanup (11.13).** The DB transaction was rolled back (nothing partial persisted),
the pool client released in `finally`, and raw-body buffers freed. Cleanup failed? Primary error
still travels; secondary logged.

**Stage 14 — Terminal? (11.16).** Not yet: `retry_pending_producer` is non-terminal and carries
`deadline_at = now + 3 days` (Stripe's window). When redelivery succeeds:
`succeeded(event_id)` — terminal. If the deadline passes: `failed(DB_UNAVAILABLE)` — terminal,
DLQ-style audit, alert. No zombie states.

**Guard rails (11.14-11.15).** On redelivery, the dedupe check observes the existing record and
returns `200` without re-executing (double-handling prevented). If the serializer crashed, the
minimal fallback body (11.15) would still return JSON with the correlation ID — Stripe's retry
logic keys off the status code, which stays `500`/`503` regardless.

## The full trace table

| Stage | Owner | Artifact | Output |
| ----- | ----- | -------- | ------ |
| 1 origin | infrastructure | driver error | pool exhaustion |
| 2 detect | repository | throw | `AppError` begins |
| 3 represent | repository | `AppError` | `DB_UNAVAILABLE` + cause |
| 4 classify | registry | code metadata | retryable `true` |
| 5 enrich | application | context fields | tenant, resource, event ID |
| 6 cause | all layers | `cause` chain | 3-link history |
| 7 propagate | layers 9.4→9.2 | unchanged error | arrives at boundary |
| 8 translate | boundary | status map | `503` |
| 9 decide | application | decision | `RETRY-THROUGH-PRODUCER` |
| 10 apply | — (external budget) | dedupe record | Stripe redelivers |
| 11 render | filter | RFC 9457 body | `503` + code + request-id |
| 12 finalize | application | `webhook_events` row | `retry_pending_producer` |
| 13 cleanup | `finally` | released resources | clean pool |
| 14 terminal (eventual) | sweeper/next delivery | `succeeded`/`failed` | terminal record |

## Key data / numbers

- Stripe webhook retries: redeliveries over up to **~3 days** with increasing backoff; a `2xx`
  acknowledges permanently; non-`2xx` triggers retry.
- Dedupe key: Stripe `event.id` — one row per event; reprocessing is a no-op.
- `503` + envelope: retryable-class rendering; Stripe does not read our body, but *we* log the
  code and correlation ID for support.
- Deadline on `retry_pending_producer`: align with the producer's retry window (~72 h) minus a
  safety margin; sweeper cadence well under an hour.
- The lifecycle cost of this incident, end to end: **~90 seconds** of customer-visible delay on
  a webhook Stripe would have retried anyway — the correct, boring outcome.

## Real-world use case — Acme SaaS

Before the lifecycle existed, this same event hit a consumer that caught everything and returned
`200 { received: true }`. The write silently failed; Stripe marked delivery complete; the
customer's invoice stayed "open" in Acme while Stripe moved to dunning. It was found **11 days
later** during a reconciliation job — after dunning emails had gone out. The traced lifecycle
above is the direct replacement: same transient failure, now visible, classified, retried by the
right owner, and terminal either way.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Producer-retry via `5xx` + dedupe (shown) | Simple; leverages Stripe's robust schedule | Latency tied to producer backoff | Most webhook consumers |
| Internal bounded retry then `200`/`500` | Faster recovery when our blip is short | Must own retry budget + idempotency | High-volume events with tight SLAs |
| Always `200`, async queue | Fast ack | Requires reliable internal queue + DLQ | When you *have* a durable queue |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide per code whether the producer or we retry | Retry inside the filter "for safety" |
| Dedupe on the producer's event ID | Re-execute the same event on redelivery |
| Finalize the attempt record before rendering | Render and forget to record |
| Give producer-pending states a deadline | Leave `retry_pending` unbounded |

## Common mistakes

- **`200` for transient failures** — the classic silent data loss; status class is the contract.
- **No dedupe** — producer redelivers a success-path duplicate and creates two side effects.
- **Treating redelivery as hostile** — redelivery is normal operation; make it a no-op, not an
  error.

## Checklist

- [ ] All 14 stages exist for your webhook consumer, with named owners.
- [ ] Transient classes route to one retry owner (producer or internal, not both).
- [ ] Event-ID dedupe makes redelivery free.
- [ ] Attempt records reach terminal states within the producer's window.

## Related

- [`ExportJob`: Retry, Compensation, Terminal](./02-exportjob-retry-compensation-terminal.md)
- [Terminal State and the Standard Lifecycle](../01-concepts/05-terminal-state-and-standard-lifecycle.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
