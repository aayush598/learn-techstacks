# Chapter 4 — Reference

> Part II · Chapter 4 · Cheat sheet, axis decision table, and glossary.

## The big taxonomy cheat-sheet

One row per category family. `HTTP` is the derived status class; `Retry` is the default verdict
before idempotency is considered.

| Family | Representative categories | HTTP | Retry | Alert | Sensitive | Owner |
| ------ | ------------------------- | ---- | ----- | ----- | --------- | ----- |
| **INPUT** | validation, request_parsing, not_found, conflict, state_transition | 4xx | no | none | no | domain |
| **AUTH** | authentication, authorization | 401/403 | no | warn | **yes** | identity |
| **BUSINESS** | business_rule, quota | 422/429 | no | none/warn | no | domain |
| **LIMIT** | rate_limit, resource_exhaustion | 429/503 | yes | warn/page | no/yes | platform |
| **DATA** | database, cache, file_storage, data_integrity | 500/502 | mixed | page/warn | **yes** | data |
| **EXTERNAL** | external_api, network, timeout | 502/503/504 | yes | warn | **yes** | integration |
| **RUNTIME** | configuration, internal_programming, unexpected_runtime | 500 | no | page | **yes** | platform |
| **ASYNC** | background_job, partial, compensation | 500 | mixed | warn/page | no | domain |
| **AI** | ai_provider, ai_token_limit, ai_tool | 502/422 | mixed | warn | no | AI |

## The fifteen classification axes

| # | Axis | Values (abridged) | Drives |
| - | ---- | ----------------- | ------ |
| 1 | Origin | client / app / datastore / dependency / runtime | Ownership |
| 2 | Severity | info / warning / error / critical / fatal | Alerting |
| 3 | Recoverability | recoverable / unrecoverable | Recover vs terminate |
| 4 | Permanence | transient / permanent | Retry |
| 5 | Affected component | api / worker / db / cache / queue / provider | Routing |
| 6 | User impact | none / degraded / blocked / data loss | Priority |
| 7 | Retry eligibility | yes / no / conditional | Retry engine |
| 8 | HTTP semantics | 400/401/403/404/409/422/429/5xx | Public contract |
| 9 | Domain/capability | billing / identity / exports / agents | Ownership, prefix |
| 10 | Security implications | sensitive / not | Redaction |
| 11 | Transactional | none / rolled_back / partial / unknown | Recovery, compensation |
| 12 | Dependency | required / optional, named | Resilience |
| 13 | Compensation | required / not | Saga path |

## Decision table — is this a category or a code?

| Question | If yes | If no |
| -------- | ------ | ----- |
| Does retry eligibility differ? | New category | New code |
| Does HTTP status class differ? | New category | New code |
| Does alert severity/routing differ? | New category | New code |
| Does disclosure/redaction differ? | New category | New code |
| Does compensation requirement differ? | New category | New code |
| None of the above differ | — | It is a **code** in an existing category |

## Decision table — choosing the primary category

| First true condition | Primary category |
| -------------------- | ---------------- |
| Defect in our code/runtime | `internal_programming` / `unexpected_runtime` / `configuration` |
| Input/contract problem | `validation` / `request_parsing` / `authentication` / `authorization` |
| Legitimate business outcome | `business_rule` / `conflict` / `state_transition` / `not_found` |
| Resource/limit reached | `rate_limit` / `quota` / `resource_exhaustion` |
| Dependency/network problem | `external_api` / `network` / `timeout` / `database` / `cache` |
| Async job / partial | `background_job` / `partial` / `compensation` |
| Nothing else fits | `unexpected_runtime` |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Taxonomy | The whole classification system (axes + hierarchy + rules) |
| Axis | A dimension along which errors are described |
| Category | One routing bucket on the primary axis |
| Code | A stable machine identifier for a specific condition |
| Tag | A non-routing descriptive property (transient, sensitive, …) |
| Primary category | The single category that drives routing |
| Family | A top-level grouping of categories |
| Precedence tree | The first-match order that picks the primary category |
| Governance | The process that lets the taxonomy change safely |
| Alias | A temporary mapping from a deprecated code to its replacement |

## Signposts

- Taxonomy in practice → [Ch. 5 Error Categories in Detail](../../05-error-categories-in-detail/README.md)
- Codes and registries → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- HTTP mapping → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)

## Related

- [Chapter 4 Do's and Don'ts](../04-dos-and-donts/README.md)
- [A Complete Taxonomy for Acme SaaS](../03-practical-examples/01-acme-error-taxonomy.md)
- [Part II Index](../../README.md)
