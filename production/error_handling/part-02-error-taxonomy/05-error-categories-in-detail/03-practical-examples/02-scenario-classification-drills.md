# Scenario Classification Drills

> Part II · Chapter 5 · Sections 5.1–5.35 (applied) · _Estimated reading time: 24 min_
> **Prerequisite:** [The Classification Decision Tree](../02-deep-dive/02-classification-decision-tree.md)

## In one sentence

Classification becomes a skill through **repetition**: take real symptoms from the recurring cast,
name the category, its code, its HTTP status, and its retry verdict — fast.

## Why this matters in production

In an incident, nobody has time to reason from first principles. Teams that have rehearsed the
mappings move straight from symptom to policy. These drills are that rehearsal.

## How to use these drills

For each scenario, fill the columns **before** reading the answer:

```text
Category | Code | HTTP | Retry | Alert | Dominant overlap
```

Then check against the key below. Do them cold; speed is the point.

## Drill 1 — `Checkout` (payments)

| # | Symptom | Category | Code | HTTP | Retry |
| - | ------- | -------- | ---- | ---- | ----- |
| 1.1 | card declined by Stripe | business_rule | `BUSINESS_CARD_DECLINED` | 422 | no |
| 1.2 | Stripe `429` on charge | rate_limit | `RATE_LIMIT_EXCEEDED` | 429 | yes |
| 1.3 | read timeout after sending charge | timeout | `TIMEOUT_OPERATION` | 504 | yes* |
| 1.4 | duplicate idempotency key, same body | duplicate_operation | `DUPLICATE_OPERATION_REPLAYED` | 200 | no |
| 1.5 | idempotency key reused, different body | duplicate_operation | `DUPLICATE_KEY_REUSED` | 409 | no |
| 1.6 | charge ok, subscription insert `23505` | duplicate_operation | `DUPLICATE_RESOURCE` | 409 | no |
| 1.7 | charge ok, DB `40001` | concurrency | `CONCURRENCY_RETRY` | 409 | yes |
| 1.8 | Stripe returns `401` | configuration | `CONFIG_DEPENDENCY_AUTH` | 500 | no |
| 1.9 | refund of already-refunded charge | state_transition | `STATE_INVALID_TRANSITION` | 409 | no |
| 1.10 | Stripe returns malformed JSON | external_api | `DEPENDENCY_INVALID_RESPONSE` | 502 | no |

\* only because `Checkout` always sends an idempotency key; without it, retry is forbidden.

## Drill 2 — `ExportJob` (long-running)

| # | Symptom | Category | Code | HTTP | Retry |
| - | ------- | -------- | ---- | ---- | ----- |
| 2.1 | S3 `SlowDown` (`503`) | file_storage | `FILE_STORAGE_THROTTLED` | 502 | yes |
| 2.2 | S3 `NoSuchKey` on input | file_storage | `FILE_STORAGE_MISSING` | 502 | no |
| 2.3 | tenant exceeds monthly export quota | quota | `QUOTA_EXPORT_LIMIT` | 429 | no |
| 2.4 | Redis unreachable mid-run | cache | `CACHE_UNAVAILABLE` | — | bypass |
| 2.5 | 900/1000 rows written then DB dies | database + partial | `DATABASE_UNAVAILABLE` | 503 | yes (remainder) |
| 2.6 | checksum mismatch on output object | data_integrity | `DATA_INTEGRITY_CHECKSUM` | 500 | no |
| 2.7 | nightly run missed during deploy | scheduled_task | `SCHEDULED_MISSED_RUN` | — | catch-up |
| 2.8 | worker OOM-killed | resource_exhaustion | `RESOURCE_EXHAUSTION` | — | bounded |
| 2.9 | deploy sends `SIGTERM` mid-run | shutdown_lifecycle | `SHUTDOWN_DRAINING` | 503 | resume |
| 2.10 | operator cancels the export | cancellation | `CANCELLATION_REQUESTED` | 499 | no |

## Drill 3 — `WebhookIngest` (inbound Stripe)

| # | Symptom | Category | Code | HTTP | Retry |
| - | ------- | -------- | ---- | ---- | ----- |
| 3.1 | signature header missing | authentication | `AUTH_SIGNATURE_MISSING` | 401 | no |
| 3.2 | signature timestamp too old (replay) | authentication | `AUTH_SIGNATURE_STALE` | 401 | no |
| 3.3 | event delivered twice (same `event.id`) | webhook + duplicate | `WEBHOOK_DUPLICATE_IGNORED` | 200 | no |
| 3.4 | event arrives out of order | webhook | `WEBHOOK_OUT_OF_ORDER` | 200 (reconcile) | no |
| 3.5 | handler throws on transient DB blip | database | `DATABASE_UNAVAILABLE` | 503 | yes (provider) |
| 3.6 | handler throws on a permanent bad payload | validation | `WEBHOOK_INVALID_PAYLOAD` | 400 | no |
| 3.7 | unknown event type | webhook | `WEBHOOK_UNHANDLED_TYPE` | 200 (ignore) | no |
| 3.8 | processing too slow, provider retries | webhook | `WEBHOOK_SLOW_ACK` | 200 (async) | n/a |

> ⚠️ Returning `5xx` for a permanent reason (3.6) creates a **poison loop**; return `400`.

## Drill 4 — `AgentRun` (LLM + tools)

| # | Symptom | Category | Code | HTTP | Retry |
| - | ------- | -------- | ---- | ---- | ----- |
| 4.1 | provider `500` | ai_provider | `AI_PROVIDER_ERROR` | 502 | yes |
| 4.2 | provider `429` | ai_provider | `AI_PROVIDER_RATE_LIMIT` | 502 | yes |
| 4.3 | `context_length_exceeded` | ai_token_limit | `AI_TOKEN_LIMIT` | 422 | no |
| 4.4 | model returns invalid JSON for schema | ai_provider | `AI_OUTPUT_INVALID` | 502 | bounded re-ask |
| 4.5 | tool call times out | ai_tool | `AI_TOOL_TIMEOUT` | 502 | yes |
| 4.6 | tool args fail validation | ai_tool | `AI_TOOL_INVALID_ARGS` | 502 | re-prompt |
| 4.7 | agent ran 12 steps, cancelled by user | cancellation | `CANCELLATION_REQUESTED` | 499 | no |
| 4.8 | retrieval (embedding) store down | external_api | `DEPENDENCY_UNAVAILABLE` | 502 | yes |
| 4.9 | unknown internal exception in orchestration | internal_programming | `INTERNAL_ERROR` | 500 | no |
| 4.10 | run billed twice on retry | partial + duplicate | `AI_SIDE_EFFECT_DUPLICATE` | — | use dedupe key |

## Scoring

| Correct | Level |
| ------- | ----- |
| 36–40 | Taxonomy fluent — help review others' classifications |
| 30–35 | Solid — revisit the overlap map |
| 20–29 | Re-read the decision tree and overlap rules |
| < 20 | Re-read the family concept files |

## Worked narrative — one incident, five categories

A tenant reports a subscription was double-charged. Trace:

```text
(1) Checkout POST timed out at 15s ................ timeout         (5.18) — outcome unknown
(2) client retried without idempotency key ........ duplicate op    (5.8)  — second charge
(3) both charges succeeded ........................ partial         (5.29) — partial completion
(4) refund of the extra charge succeeded .......... compensation    (5.30) — logical undo
(5) root cause: env var for key was unset ......... configuration   (5.20) — fix + alert
```

The fix is not "handle timeouts better"; it is **enforce an idempotency key (configuration)** so
the ambiguous outcome in step 1 becomes safe to retry.

## Key data / numbers

- `duplicate_operation` → `200` on **replay**; `409` only when the key is **reused with a different
  body**.
- Webhook permanent failures must return `4xx`; transient ones `5xx` (provider-driven retry).
- `cancellation` is `499`/`INFO`; never `500`/`error`.
- Token limits (`ai_token_limit`) are `422`/permanent; provider errors are `502`/retryable.

## Real-world use case — Acme SaaS on-call training

Acme used these four drills as an onboarding exercise. New engineers classified 40 scenarios in
under 30 minutes; the incident-channel MTTR for misclassification dropped because responders
agreed on category → policy without debate. The drills are now part of the error-handling
onboarding checklist.

## Trade-offs

| Drill style | Pros | Cons |
| ----------- | ---- | ---- |
| Cold table fill | Fast recall | Needs a key |
| Live incident review | Real | Unpredictable |
| Automated fixtures | Regression-safe | Setup cost |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Rehearse overlap cases | Memorize without the "why" |
| Score and re-drill weak areas | Skip the ambiguous ones |
| Turn answers into fixtures | Let drills stay paper-only |
| Include the recurring cast | Use only abstract examples |

## Common mistakes

- **Choosing by HTTP status** instead of cause (`429` quota vs rate limit).
- **Forgetting idempotency** when marking a timeout retryable.
- **Marking partial as complete.**
- **Returning `5xx`** for permanent webhook failures.

## Checklist

- [ ] Can you classify a random symptom in under 15 seconds?
- [ ] Do you disambiguate shared statuses by code?
- [ ] Do you always fold in idempotency for retry verdicts?
- [ ] Are your drill answers encoded as unit-test fixtures?

## Related

- [The Full Category Catalog in Code](./01-taxonomy-in-code.md)
- [Category Interactions and Overlaps](../02-deep-dive/01-category-interactions-and-overlaps.md)
- [Chapter 5 Reference Cheat-Sheet](../05-reference/README.md)
