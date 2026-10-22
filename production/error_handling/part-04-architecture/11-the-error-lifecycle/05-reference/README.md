# Chapter 11 — Reference

> Part IV · Chapter 11 · Lifecycle cheat sheet, handling decision table, glossary, and signposts.
> _Estimated reading time: 12 min_

## Lifecycle stages cheat sheet

| # | Stage | Question it answers | Owner | Artifact / output | § |
| - | ----- | ------------------- | ----- | ----------------- | - |
| 1 | **Origin** | Where did the deviation start? | The code at the origin | Fault, bad input, or dependency error | 11.1 |
| 2 | **Detect** | When does it become an error *value*? | Detecting layer | Throw, `Result.Err`, failed assertion | 11.2 |
| 3 | **Represent** | What is the standard internal shape? | Detecting layer, at the boundary | `AppError { code, cause }` | 11.3 |
| 4 | **Classify** | What kind of error is it? | Registry | `category`, `retryable`, `severity` | 11.4 |
| 5 | **Enrich** | What safe facts help triage? | Each ascending layer | Allowlisted context fields | 11.5 |
| 6 | **Preserve cause** | What history must survive? | Every wrapper/translator | `cause` chain to the origin | 11.6 |
| 7 | **Propagate** | How does it move up? | Layers | Same error, unchanged outcome | 11.7 |
| 8 | **Translate** | Which vocabulary applies here? | Boundary owner | Mapped code, status class, envelope | 11.8 |
| 9 | **Decide** | Retry, compensate, degrade, or abort? | The one named decider | `Decision` with reason | 11.9 |
| 10 | **Apply** | Execute the verdict within budget | Decider / saga owner | Attempts or compensation steps | 11.10 |
| 11 | **Render** | What does the outside world see? | Entry-point renderer | HTTP envelope or attempt record | 11.11 |
| 12 | **Finalize** | What durable record ends the operation? | Application / worker | Terminal record | 11.12 |
| 13 | **Cleanup** | What must be released? | Resource owner (`finally`/`defer`) | Released tx, locks, uploads, streams | 11.13 |
| 14 | **Terminal** | Can anything reopen this outcome? | Storage state machine | Immutable terminal state | 11.16 |
| G | **Guard rails** | Handled once? Handler failed safely? | Decider + handler | `handled` marker, minimal fallback | 11.14–11.15 |

**Rule of thumb:** every stage has exactly one owner and one artifact. If you cannot name both,
the stage is implicit and will eventually be skipped.

## Where does this error get handled?

| Situation | Decide / handle at | Render or record | ⚠️ Watch out |
| --------- | ------------------ | ---------------- | ------------ |
| Malformed request, bad field | Transport/middleware (reject) | `4xx` problem details | Do not let parsing errors reach the domain |
| Missing/expired credentials | Auth middleware | `401` | Do not reveal whether the account exists |
| Insufficient permission / wrong tenant | Authz middleware | `403` (or `404` for existence hiding) | Never fall through to business logic |
| Domain invariant or business rule | Application service | `409`/`422` via the code map | Expected outcome; do not retry |
| Persistence driver error (`23505`, `40001`) | Repository translates; application decides | `409`/`503` | Preserve SQLSTATE as `cause` |
| Transient dependency error (`429`, `503`, timeout) | Application service or worker | Retry within budget, then `503`/DLQ | Retry only idempotent steps; honor `Retry-After` |
| Failure after a completed side effect | Saga owner | Compensation, then terminal | Compensation is a new, idempotent operation |
| Job attempt failure | Worker (queue consumer) | Attempt record, delayed retry, DLQ | One decider — not the worker *and* the broker |
| Webhook processing failure | Webhook application service | `5xx` to producer *or* internal retry | Pick one retry owner; dedupe on `event.id` |
| Unknown / unclassified error | Global handler (mechanical only) | `500` + correlation ID | Never branch on message text |
| Failure while handling | Nested containment ladder | Fixed minimal body + level-0 log | Each level must be simpler than the last |
| Cleanup / release failure | Cleanup owner | Log as secondary; keep primary outcome | Never replace the primary error |
| Ambiguous commit or charge | Application service, then read back | Terminal *after* verification | Never guess `failed` when success is possible |
| Canceled by client, shutdown, or deadline | Application service / worker | `canceled` terminal state | Cancellation is not success and not failure |

## Who owns which stage, per entry point

| Entry point | Decider | Renderer | Terminal record |
| ----------- | ------- | -------- | --------------- |
| HTTP request (`Checkout`) | Application service | Controller / error filter | Operation or payment row |
| Background job (`ExportJob`) | Worker | Attempt record + DLQ | Job row |
| Inbound webhook (`WebhookIngest`) | Webhook application service | `2xx`/`5xx` to the producer | `webhook_events` row |
| LLM tool run (`AgentRun`) | Run orchestrator | Run/step record | `agent_runs` row |

## Numbers to standardize

| Setting | Recommendation | Notes |
| ------- | -------------- | ----- |
| Max retry attempts | **5** | Unknown errors: 1 retry, then DLQ |
| Backoff | Base ~2 s, factor 2, full jitter | Respect server `Retry-After` when present |
| Total deadline | Attempts × delay ≤ operation deadline | Must fit inside the visibility timeout |
| Cleanup budget | **≤ 5–10 s** total | Kubernetes default grace is **30 s** |
| Job heartbeat | ~10 s; expire after **2–3** misses | Sweeper converts to `failed(ABANDONED)` |
| DLQ write retries | ~3, then terminate the process | Redelivery beats losing the message |
| `Retry-After` suggestion | 30–120 s for provider blips | Tell the client a realistic window |
| Webhook retry window | ~3 days (producer-dependent) | Put a deadline on any pending state |

## Terminal vocabulary

```text
succeeded | failed(code) | compensated(code) | canceled(reason)
failed_retries_exhausted(code, dlqRef)
```

Five values, no ad-hoc strings. `pending`, `running`, `retry_scheduled`, and `compensating` are
**stages**, not states of rest — each needs a lease or deadline that forces a terminal outcome.
Replay is a **new operation** referencing the old record, never a resurrection.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Origin** | The point where the deviation begins: input, domain computation, persistence, dependency, concurrency, runtime, or a bug |
| **Detection** | The moment the deviation becomes an error value the program can act on |
| **Representation** | Converting an error into the application's standard model (`code`, category, `cause`, context) |
| **Classification** | Attaching the axes that drive later decisions: category, retryability, severity, terminality, public visibility |
| **Enrichment** | Adding allowlisted, non-sensitive context as the error moves upward |
| **Cause chain** | The linked history of originals beneath every wrapper, used for logs and triage |
| **Propagation** | Moving an error up the call stack or across async boundaries without changing its outcome |
| **Translation** | Swapping vocabulary at a boundary (driver → domain → transport) while preserving meaning and cause |
| **Decider** | The single owner that chooses retry, compensate, degrade, or abort for an operation |
| **Recovery verdict** | The decider's recorded choice and reason, applied in stage 10 |
| **Compensation** | A new, idempotent operation that logically undoes a completed step |
| **Renderer** | The entry-point component that converts a decided outcome into a protocol response or attempt record |
| **Finalization** | The durable record that an operation is over and how it ended |
| **Terminal state** | An outcome that no further lifecycle action may change |
| **Double handling** | Two layers or entry points deciding or acting on the same failure |
| **Containment ladder** | The ordered fallbacks used when the error handler itself fails: original → handler → minimal body → process boundary |
| **Abandoned** | A `running` operation whose lease expired; swept to `failed(ABANDONED)` |
| **Ambiguous outcome** | A failure where success is possible (e.g. crash during commit); resolve by read-back |
| **Handle-once ledger** | The documented mapping from code to the one layer allowed to decide it |

## Signposts

- Origins and classification axes → [Chapter 4](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md) and [Chapter 5](../../../part-02-error-taxonomy/05-error-categories-in-detail/README.md)
- Internal error model and registry → [Chapter 6](../../../part-03-error-models/06-designing-the-applications-error-model/README.md) and [Chapter 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- Layer placement and translation points → [Chapter 9](../../09-layered-error-handling-architecture/README.md)
- Central vs local handling → [Chapter 10](../../10-centralized-and-distributed-error-handling/README.md)
- Cleanup mechanics → [Chapter 14](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
- Retries and idempotency → [Chapter 27](../../../part-11-retry-and-resilience/27-retry-policies/README.md) and [Chapter 28](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- Jobs and webhooks → [Chapter 32](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md) and [Chapter 33](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- Async propagation → [Chapter 31](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)

## Related

- [Chapter 11 Do's and Don'ts](../04-dos-and-donts/README.md)
- [The Lifecycle: Origin Through Classification](../01-concepts/01-lifecycle-overview.md)
- [`WebhookIngest`: One Failure Through the Whole Lifecycle](../03-practical-examples/01-webhookingest-lifecycle-walkthrough.md)
- [Part IV Index](../../README.md)
- [Shared Glossary](../../../GLOSSARY.md)
