# Chapter 5 — Reference

> Part II · Chapter 5 · Big category cheat-sheet with codes, HTTP mapping, and retry policy.

## The big category cheat-sheet (all 35)

| # | Category | Typical code | HTTP | Retry | Alert | Sensitive |
| - | -------- | ------------ | ---- | ----- | ----- | --------- |
| 5.1 | validation | `VALIDATION_*` | 422 | no | none | no |
| 5.2 | request parsing | `REQUEST_MALFORMED_JSON` | 400 | no | none | no |
| 5.3 | authentication | `AUTH_INVALID_CREDENTIALS` | 401 | no | warn | **yes** |
| 5.4 | authorization | `AUTHZ_INSUFFICIENT_SCOPE` | 403 | no | warn | **yes** |
| 5.5 | business rule | `BUSINESS_CARD_DECLINED` | 422 | no | none | no |
| 5.6 | not found | `RESOURCE_NOT_FOUND` | 404 | no | none | no |
| 5.7 | conflict | `CONFLICT_VERSION_MISMATCH` | 409 | no | none | no |
| 5.8 | duplicate operation | `DUPLICATE_KEY_REUSED` | 409/200 | no | none | no |
| 5.9 | state transition | `STATE_INVALID_TRANSITION` | 409 | no | none | no |
| 5.10 | rate limiting | `RATE_LIMIT_EXCEEDED` | 429 | **yes** | warn | no |
| 5.11 | quota / usage limit | `QUOTA_EXPORT_LIMIT` | 429/402 | no | warn | no |
| 5.12 | concurrency / optimistic lock | `CONCURRENCY_RETRY` | 409/412 | **yes** | warn | **yes** |
| 5.13 | database | `DATABASE_UNAVAILABLE` | 503 | mixed | page | **yes** |
| 5.14 | cache | `CACHE_UNAVAILABLE` | 500 | no (bypass) | warn | **yes** |
| 5.15 | file storage | `FILE_STORAGE_MISSING` | 502 | mixed | warn | **yes** |
| 5.16 | external API | `DEPENDENCY_UNAVAILABLE` | 502 | **yes** | warn | **yes** |
| 5.17 | network / connectivity | `NETWORK_UNREACHABLE` | 503 | **yes** | warn | **yes** |
| 5.18 | timeout | `TIMEOUT_OPERATION` | 504 | yes* | warn | no |
| 5.19 | serialization | `SERIALIZATION_INVALID` | 400 | no | warn | no |
| 5.20 | configuration | `CONFIG_DEPENDENCY_MISSING` | 500 | no | page | **yes** |
| 5.21 | dependency initialization | `DEPENDENCY_INIT_FAILED` | 500 | no | page | **yes** |
| 5.22 | resource exhaustion | `RESOURCE_EXHAUSTION` | 503 | bounded | page | **yes** |
| 5.23 | background job | `JOB_FAILED` | 500 | yes | warn | no |
| 5.24 | scheduled task | `SCHEDULED_MISSED_RUN` | 500 | yes | warn | no |
| 5.25 | internal programming | `INTERNAL_ERROR` | 500 | no | page | **yes** |
| 5.26 | unexpected runtime | `INTERNAL_ERROR` | 500 | no | page | **yes** |
| 5.27 | cancellation / interruption | `CANCELLATION_REQUESTED` | 499 | no | none | no |
| 5.28 | data integrity | `DATA_INTEGRITY_*` | 500 | no | page | **yes** |
| 5.29 | partial completion | `PARTIAL_COMPLETION` | 500/207 | resume | page | no |
| 5.30 | compensation / rollback | `COMPENSATION_FAILED` | 500 | until applied | page | no |
| 5.31 | shutdown / lifecycle | `SHUTDOWN_DRAINING` | 503 | resume | warn | no |
| 5.32 | third-party dependency | `DEPENDENCY_UNAVAILABLE` | 502 | yes* | warn | **yes** |
| 5.33 | AI model / tool / token limit | `AI_PROVIDER_ERROR` | 502/422 | mixed | warn | no |
| 5.34 | webhook delivery / processing | `WEBHOOK_*` | 400/200 | provider | warn | **yes** |
| 5.35 | file upload / processing | `FILE_*` | 413/415/422 | mixed | warn | no |

\* retry only if the operation is idempotent.

## Signal → category quick map

| Real signal | Category |
| ----------- | -------- |
| `422` on a valid-looking body | validation |
| `400` malformed JSON | request parsing |
| `401` with `WWW-Authenticate` | authentication |
| `403 insufficient_scope` | authorization |
| `card_declined` | business rule |
| `404` / `410` | not found |
| `409` + `ETag` mismatch | conflict |
| `23505 unique_violation` | duplicate operation |
| `409` + lifecycle state | state transition |
| `429` + `Retry-After` | rate limit |
| `429`/`402` + plan code | quota |
| `40001`, `40P01` | concurrency |
| `23502`, `23503`, `23514`, `08xxx`, `53300` | database |
| Redis `LOADING`/`READONLY`/`CLUSTERDOWN` | cache |
| S3 `SlowDown`/`NoSuchKey`/`AccessDenied` | file storage |
| provider `5xx`/`429` | external API |
| `ECONNRESET`, `ENOTFOUND`, `ECONNREFUSED` | network |
| we stopped waiting | timeout |
| JSON/schema parse failure | serialization |
| missing/invalid env or secret | configuration |
| client boot dep unreachable | dependency initialization |
| `EMFILE`, `ENOMEM`, `ENOSPC`, pool exhaustion | resource exhaustion |
| `TypeError`, `NPE`, assertion | internal programming |
| unknown/uncategorized | unexpected runtime |
| `context canceled`, `499`, `CANCELLED(1)` | cancellation |
| `SIGTERM` draining | shutdown / lifecycle |
| `finish_reason=length`, `context_length_exceeded` | AI token limit |
| bad webhook signature | webhook (+ authentication) |
| `413`/`415` on upload | file upload |

## Family grouping

| Family | Categories |
| ------ | ---------- |
| **Input / auth / business** | validation, request_parsing, authentication, authorization, business_rule, not_found, conflict, duplicate_operation, state_transition |
| **Limits / concurrency / data** | rate_limit, quota, concurrency, database, cache, file_storage, data_integrity |
| **External / network / config** | external_api, network, timeout, serialization, configuration, dependency_initialization, third_party |
| **Runtime / resources / lifecycle** | resource_exhaustion, internal_programming, unexpected_runtime, cancellation, shutdown_lifecycle |
| **Async / partial / specialized** | background_job, scheduled_task, partial, compensation, ai_provider, ai_tool, ai_token_limit, webhook, file_processing |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Dominant category | The one category chosen when several apply |
| Replay | Returning the original result for a duplicate idempotent request |
| Poison message | A message that always fails and blocks a queue without a DLQ |
| Ambiguous outcome | A timeout/cancel where the write may or may not have applied |
| Compensation | A logical undo of a completed step |
| Terminal state | A job/flow state from which no further progress is expected |
| Bypass | Skipping an optional dependency (cache) rather than failing |

## Signposts

- Taxonomy design → [Ch. 4](../../04-designing-a-comprehensive-error-taxonomy/README.md)
- Codes and registries → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- HTTP mapping → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- DB categories → [Ch. 22](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
- External categories → [Ch. 25](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- Jobs and webhooks → [Ch. 32](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)

## Related

- [Chapter 5 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Scenario Classification Drills](../03-practical-examples/02-scenario-classification-drills.md)
- [Part II Index](../../README.md)
