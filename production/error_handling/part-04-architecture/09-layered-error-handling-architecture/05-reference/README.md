# Chapter 9 — Reference

> Part IV · Chapter 9 · Cheat sheets, decision tables, and the layer matrix.

## Cheat sheet — the layer matrix (9.1–9.13)

| # | Layer | Error job | Owns | Must never |
| - | ----- | --------- | ---- | ---------- |
| 9.1 | Presentation | Render | UI state for every category | Contain business rules |
| 9.2 | Transport | Reject early | Parse, authn/authz, rate limit, size/type | Interpret business meaning |
| 9.3 | Controller | Map | Outcome → status/body, correlation ID | Retry; decide business policy |
| 9.4 | Application | Decide | Retry / compensate / abort; transaction | Leak vendor or HTTP types |
| 9.5 | Domain | Declare | Invariants, business rules | Know SQL, HTTP, Stripe |
| 9.6 | Repository | Translate | Driver → persistence errors; no-row vs failed | Decide policy; invent business codes |
| 9.7 | Infrastructure | Surface | Pools, drivers, config, object storage | Imply domain meaning |
| 9.8 | Integration | Normalize | Vendor → stable internal codes + retryability | Expose vendor shapes upward |
| 9.9 | Background worker | Classify + schedule | Attempts, backoff, DLQ | Contain domain rules |
| 9.10 | Scheduled task | Guard | Overlap, idempotent re-run, run record | Assume last run succeeded |
| 9.11 | Bootstrap | Halt | Config/dep validation, fail fast, exit code | Serve half-wired |
| 9.12 | Process boundary | Terminate | Crash, OOM, signals | Attempt in-process recovery |

## Cheat sheet — the three verbs (9.16–9.18)

```text
HANDLE      change the OUTCOME   → one layer per error (application / worker / transport)
TRANSLATE   change the SHAPE     → once per boundary, cause preserved
PROPAGATE   change nothing       → default; add context only
```

## Cheat sheet — translation points (9.13)

| ID | From → To | Where | Example |
| -- | --------- | ----- | ------- |
| T1 | driver → persistence | `infra/postgres/*-repo.ts` | `23505` → `DUPLICATE_KEY` |
| T2 | vendor → internal | `integration/*` | `StripeCardError` → `PAYMENT_CARD_DECLINED` |
| T3 | OS/FS/config → operational | `infra/*` | ENOENT → `CONFIG_MISSING` |
| T4 | mixed → normalized | `app/normalize.ts` | any → `AppError` with retryability |
| T5 | outcome → HTTP | `http/problem.ts` | `DUPLICATE_KEY` → `409` + RFC 9457 |
| T6 | outcome → job record | `workers/attempt.ts` | retryable → backoff; terminal → DLQ |

## Decision table — handle or translate or propagate?

| Situation | Verb | Layer |
| --------- | ---- | ----- |
| Body fails schema | Handle (reject) | transport / controller |
| Auth missing or bad | Handle (reject) | transport |
| Domain invariant violated | Propagate, then map | domain → controller |
| `SQLSTATE` raised | Translate | repository |
| Stripe error object raised | Translate | integration |
| Retryable error arrives | Handle (decide retry) | application / worker |
| Error arrives with no new decision available | Propagate | anywhere in between |
| Job attempts exhausted | Handle (DLQ) | worker |
| Config invalid at boot | Handle (halt) | bootstrap |
| Unclassified escapee | Handle (safety net) | global handler / process |

## Cheat sheet — external shapes by layer

| Layer | HTTP shape | Job shape |
| ----- | ---------- | --------- |
| transport | `400/401/403/405/413/415/429` | n/a |
| controller | `402/404/409/422/500/502/503/504` | n/a |
| worker | n/a | ack / retry(delay) / fail(dlq) |
| scheduler | n/a | succeeded / failed / skipped_overlap |
| bootstrap | none (no listener yet) | exit code 1 |
| process | connection reset (unavoidable) | orchestrator restart |

## Handle-once ledger template

| Code | Origin | Handling layer | HTTP | Job | Retryable |
| ---- | ------ | -------------- | ---- | --- | --------- |
| `WORKSPACE_SLUG_TAKEN` | repo | application | `409` | terminal | no |
| `SEAT_LIMIT_REACHED` | domain | application | `409` | terminal | no |
| `UPSTREAM_RATE_LIMITED` | integration | application | `429` | delayed retry | yes |
| `DB_UNAVAILABLE` | infra | application | `503` | delayed retry | yes |
| `PAYMENT_CARD_DECLINED` | integration | application | `402` | terminal | no |
| `RATE_LIMITED` (local) | transport | transport | `429` | n/a | yes |
| unclassified | any | global handler | `500` | 1 retry → DLQ | ⚠️ |

## Key numbers to remember

- Transport statuses: `400 401 403 405 413 415 429`.
- Postgres codes confined to T1: `23505 23503 23502 40001 40P01 53300 08xxx`.
- Recommended job attempts: **5**, backoff base **~2 s** (factor 2, jitter), DLQ on terminal.
- Bootstrap: exit **1**; Kubernetes `SIGTERM` grace **30 s** (default).
- Retry amplification: N layers × M attempts = N·M upstream calls — keep N = 1.

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Layer | A role in the request/job path with one error job |
| Translation point | The named place where an error's representation changes |
| Handle-once ledger | Table: one handling layer per error code |
| Vocabulary narrowing | Each layer emits fewer, more stable codes than it accepts |
| Closure | A layer never emits a representation it also accepts |
| Entry-point consistency | Same fault → same stable code, regardless of path |

## Signposts

- Boundaries in depth → [Ch. 15 Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- Translation mechanics → [Ch. 16 Error Translation](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- Job policies → [Ch. 32 Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- Process failures → [Ch. 41 Process & Runtime](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)

## Related

- [Chapter 9 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part IV Index](../../README.md)
