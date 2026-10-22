# Category Interactions and Overlaps

> Part II · Chapter 5 · Sections 5.1–5.35 · _Estimated reading time: 24 min_
> **Prerequisite:** [Input, Auth, and Business Categories](../01-concepts/01-input-auth-and-business-errors.md)

## In one sentence

Real failures belong to **two or three categories at once**; the skill is knowing which pairs are
commonly confused and applying a fixed rule to pick the **dominant** one.

## Why this matters in production

Misclassification is rarely about missing a category — it is about choosing the wrong one among
overlapping candidates. A retried webhook can look like `conflict`, `duplicate`, or `webhook`. A
slow DB can look like `timeout`, `database`, or `network`. Each wrong choice routes to the wrong
policy. This file is the disambiguation guide.

## Core concept — dominant category rules

```text
Rule 1: Classify by CAUSE, not by symptom or status.
Rule 2: Prefer the MORE SPECIFIC category when both apply.
Rule 3: Prefer the category that determines the POLICY (retry/compensation).
Rule 4: Everything else becomes a TAG, not a second category.
```

## The overlap map

| Confusable pair | Distinguisher | Dominant | The other is… |
| --------------- | ------------- | -------- | ------------- |
| validation vs business_rule | syntactic/schema vs domain rule | see below | tag `semantic` |
| authentication vs authorization | who are you vs what may you do | both distinct | — |
| conflict vs duplicate_operation | state conflict vs same op twice | cause | — |
| conflict vs state_transition | any conflict vs lifecycle-specific | state_transition (specific) | — |
| rate_limit vs quota | transient throttle vs permanent limit | cause | — |
| timeout vs network | we stopped waiting vs connection fault | timeout if we set it | tag `network` |
| timeout vs external_api | timeout is a mechanism | external_api if remote error known | — |
| database vs concurrency | constraint vs serialization race | concurrency for `40001`/`40P01` | tag `database` |
| cache vs database | optional vs source of truth | source of truth on error | tag `cache` |
| serialization vs external_api | our parse vs remote contract | external_api if remote's fault | — |
| cancellation vs timeout | initiator left vs we gave up | cancellation | — |
| partial vs background_job | state vs container | partial (state) | tag `job` |
| compensation vs background_job | action vs container | compensation | tag `job` |
| webhook vs duplicate_operation | channel vs nature | webhook (channel) | tag `duplicate` |
| ai_provider vs external_api | modality vs generic | ai_provider (specific) | tag `external` |
| file_processing vs validation | file content vs request | file_processing (specific) | tag `validation` |

## Deeper disambiguation

### conflict vs duplicate vs concurrency

- **conflict** — the request conflicts with state (version, already-exists, has-dependents).
- **duplicate_operation** — the *same* operation resubmitted (idempotency domain).
- **concurrency** — two writers raced; the DB rejected one (`40001`/`40P01`), retryable.

```text
A unique constraint 23505 on INSERT:
  Is it a retried idempotent request? → duplicate_operation (replay)
  Is it a genuine second attempt to create? → conflict (already exists)
  Never → concurrency (that's serialization/deadlock, not unique)
```

### timeout vs network vs external_api

```text
ECONNREFUSED before send      → network (connect)        → retry, not ambiguous
read timeout after send       → timeout (ambiguous)      → retry only if idempotent
provider returned 500         → external_api             → retry
we killed it at our deadline  → timeout                  → NOT the provider's fault
client disconnected first     → cancellation             → not a failure
```

### partial vs the operation's own error

Partial completion is a **state**, layered on top of whatever error stopped progress:

```text
ExportJob wrote 900/1000 rows, then DB 40001:
  primary  = database (transient)         → retry the remainder
  tag      = partial                      → record 900 done
  NEVER    = mark whole export "failed" and redo all 1000
```

## Worked example — classifying a redelivered webhook that errors

```text
Stripe redelivers invoice.paid; our handler throws on a duplicate insert (23505).

Candidates: webhook, duplicate_operation, conflict, database
Dominant:   webhook        (the channel/context; routing goes to WebhookIngest)
Primary category for policy: duplicate_operation (dedupe by event id → replay success)
Tags:       ["external", "transient? no", "duplicate"]
Outcome:    return 200 (already processed) — do NOT 500 (poison loop)
```

The **routing** category (webhook) and the **policy** category (duplicate) can differ, but the
taxonomy records both: one as primary, one as tag/attribute.

## Nested overlaps — one failure, a layered stack

Some failures are genuinely layered. Record them as **one primary + several tags**, not as
multiple categories:

```text
A scheduled ExportJob (scheduled_task) that hit a DB race (concurrency) while
another instance ran, after a deploy restart (shutdown_lifecycle):

primary = concurrency        (the thing to act on now)
tags    = [scheduled, partial, shutdown, database]
```

The tag stack is what dashboards filter on; the primary is what the retry engine and HTTP mapper
read. Trying to express the stack as "which of the four categories is it?" is the wrong question —
all four are true, but only one drives the immediate action.

## Key data / numbers

- PostgreSQL `40001`/`40P01` → `concurrency`; `23505` → `duplicate_operation` or `conflict`
  depending on intent; `23503` on delete → `conflict`.
- HTTP `409` is shared by conflict, duplicate, and state transition — the **code** disambiguates.
- `429` is shared by rate limit and quota — the **code** disambiguates.

## Real-world use case — Acme SaaS

Acme's global handler classified every `409` as `conflict`, so idempotent replays were returned as
errors and clients retried, spawning more duplicates. The overlap rules split `409` by code:
`CONFLICT_VERSION_MISMATCH` stays `conflict`, `DUPLICATE_KEY_REUSED` becomes
`duplicate_operation` → replay. Client retry storms dropped sharply.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| One primary + tags | Deterministic | Needs a rules doc |
| Multiple equal categories | "Complete" | Ambiguous routing |
| Route by HTTP status | Simple | Wrong for shared statuses |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify by cause | Classify by status or message |
| Prefer the more specific category | Collapse `ai_provider` into `external_api` |
| Keep extra axes as tags | Create a combined hybrid category |
| Document the dominant rules | Leave overlap to each engineer |

## Common mistakes

- **Treating `409` as always `conflict`**, breaking idempotent replay.
- **Calling a DB race `database`** when it is `concurrency` (retryable).
- **Calling a provider timeout `network`** when we set the deadline (`timeout`).
- **Marking partial work as failed**, forcing redo.

## Checklist

- [ ] Are shared HTTP statuses disambiguated by code?
- [ ] Is cause, not symptom, the classifier?
- [ ] Are secondary axes stored as tags?
- [ ] Is partial completion modeled as a state, not a category replacement?

## Related

- [Classification Decision Tree](./02-classification-decision-tree.md)
- [Async Jobs, Partial Failure, and Specialized Categories](../01-concepts/05-async-jobs-partial-and-specialized.md)
- [The Multi-Axis Classification Model (Ch. 4)](../../04-designing-a-comprehensive-error-taxonomy/02-deep-dive/01-multi-axis-classification-model.md)
