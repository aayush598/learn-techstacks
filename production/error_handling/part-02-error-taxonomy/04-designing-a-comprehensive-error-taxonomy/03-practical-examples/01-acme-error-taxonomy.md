# A Complete Taxonomy for Acme SaaS

> Part II · Chapter 4 · Sections 4.1–4.18 (applied) · _Estimated reading time: 22 min_
> **Prerequisite:** [The Multi-Axis Classification Model](../02-deep-dive/01-multi-axis-classification-model.md)

## In one sentence

Here is a **complete, real taxonomy** for the recurring cast — families, categories, codes,
HTTP mapping, and policy — the artifact you actually commit to the repository.

## Why this matters in production

A taxonomy in prose is not a taxonomy; it is documentation. The version that survives is a
**reviewable data file** every service imports. This file shows the shape of that artifact and
demonstrates how the axes from Chapter 4 collapse into a concrete table.

## The taxonomy (data file)

```yaml
# error-taxonomy.yaml — single source of truth, owned by platform, reviewed by domain teams
version: 1
families:
  INPUT:
    categories:
      validation:        { http: 422, retry: false, alert: none,  sensitive: false }
      request_parsing:   { http: 400, retry: false, alert: none,  sensitive: false }
      not_found:         { http: 404, retry: false, alert: none,  sensitive: false }
      conflict:          { http: 409, retry: false, alert: none,  sensitive: false }
      state_transition:  { http: 409, retry: false, alert: none,  sensitive: false }
  AUTH:
    categories:
      authentication:    { http: 401, retry: false, alert: warn,  sensitive: true }
      authorization:     { http: 403, retry: false, alert: warn,  sensitive: true }
  BUSINESS:
    categories:
      business_rule:     { http: 422, retry: false, alert: none,  sensitive: false }
      quota:             { http: 429, retry: false, alert: warn,  sensitive: false }
  LIMIT:
    categories:
      rate_limit:        { http: 429, retry: true,  alert: warn,  sensitive: false }
      resource_exhaustion:{ http: 503,retry: true,  alert: page,  sensitive: true }
  DATA:
    categories:
      database:          { http: 500, retry: true,  alert: page,  sensitive: true }
      cache:             { http: 500, retry: false, alert: warn,  sensitive: true }
      file_storage:      { http: 502, retry: true,  alert: warn,  sensitive: true }
      data_integrity:    { http: 500, retry: false, alert: page,  sensitive: true }
  EXTERNAL:
    categories:
      external_api:      { http: 502, retry: true,  alert: warn,  sensitive: true }
      network:           { http: 503, retry: true,  alert: warn,  sensitive: true }
      timeout:           { http: 504, retry: true,  alert: warn,  sensitive: false }
  RUNTIME:
    categories:
      configuration:     { http: 500, retry: false, alert: page,  sensitive: true }
      internal_programming:{ http: 500,retry: false, alert: page,  sensitive: true }
      unexpected_runtime:{ http: 500, retry: false, alert: page,  sensitive: true }
  ASYNC:
    categories:
      background_job:    { http: 500, retry: true,  alert: warn,  sensitive: false }
      partial:           { http: 500, retry: false, alert: page,  sensitive: false }
      compensation:      { http: 500, retry: false, alert: page,  sensitive: false }
```

## The public code catalog

Only a subset becomes **public** codes (Chapters 8, 49). Internal categories stay internal.

| Code | Category | HTTP | Retry | Public |
| ---- | -------- | ---- | ----- | ------ |
| `VALIDATION_REQUIRED_FIELD` | validation | 422 | no | ✅ |
| `REQUEST_MALFORMED_JSON` | request_parsing | 400 | no | ✅ |
| `RESOURCE_NOT_FOUND` | not_found | 404 | no | ✅ |
| `CONFLICT_VERSION_MISMATCH` | conflict | 409 | no | ✅ |
| `STATE_INVALID_TRANSITION` | state_transition | 409 | no | ✅ |
| `AUTH_INVALID_CREDENTIALS` | authentication | 401 | no | ✅ |
| `AUTHZ_INSUFFICIENT_SCOPE` | authorization | 403 | no | ✅ |
| `BUSINESS_CARD_DECLINED` | business_rule | 422 | no | ✅ |
| `QUOTA_EXPORT_LIMIT` | quota | 429 | no | ✅ |
| `RATE_LIMIT_EXCEEDED` | rate_limit | 429 | yes | ✅ |
| `DATABASE_UNAVAILABLE` | database | 503 | yes | ❌ |
| `DEPENDENCY_UNAVAILABLE` | external_api | 502 | yes | ✅ |
| `INTERNAL_ERROR` | unexpected_runtime | 500 | no | ✅ |

## Applying it — one endpoint

`POST /v1/exports` can produce a small subset. The table is the *entire* policy surface:

| Trigger | Category | Code | HTTP | Retry |
| ------- | -------- | ---- | ---- | ----- |
| missing `dateFrom` | validation | `VALIDATION_REQUIRED_FIELD` | 422 | no |
| `dateFrom > dateTo` | validation | `VALIDATION_RANGE_INVERTED` | 422 | no |
| tenant has ≥ N active exports | quota | `QUOTA_EXPORT_LIMIT` | 429 | no |
| queue publish fails | external_api | `DEPENDENCY_UNAVAILABLE` | 502 | yes |
| unhandled exception | unexpected_runtime | `INTERNAL_ERROR` | 500 | no |

The endpoint code contains **no** `if status === ...` logic — it throws classified errors and the
edge translates.

## Worked example — adding a new capability

Acme adds `AgentRun` (LLM). The team wants `AI_*` codes. Applying the growth test (Section 4.17):
the retry/alert/disclosure profile differs from `external_api` (partial output, non-determinism,
degradation), so a new **category family `AI`** is justified — but only three categories:
`ai_provider`, `ai_token_limit`, `ai_tool`. Everything else stays a code.

```yaml
AI:
  categories:
    ai_provider:   { http: 502, retry: true,  alert: warn, sensitive: false }
    ai_token_limit:{ http: 422, retry: false, alert: none, sensitive: false }
    ai_tool:       { http: 502, retry: true,  alert: warn, sensitive: false }
```

## Key data / numbers

- Acme's full taxonomy: **9 families, ~30 categories, ~120 codes**, of which ~25 are public.
- The entire handling logic for any endpoint is a lookup into the table above.
- Registry size grows with features, but **family count stays flat** — the sign of a healthy
  taxonomy.

## Real-world use case — Acme SaaS

Acme stored this file in the platform repo, imported by the API gateway, four workers, and the
frontend codegen. When a new `quota` policy was needed, it changed **one line** in the YAML and
every service picked it up on deploy. Before the taxonomy, the same change meant edits in six
repositories. This is the compounding return on classification.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| YAML table | Reviewable, shared | Needs a loader |
| Code enum per service | Type-safe locally | Drifts across services |
| Docs only | Zero setup | No enforcement |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep policy as data | Hard-code policy per service |
| Mark which codes are public | Expose all internal codes |
| Add families rarely | Add a family per feature |
| Derive endpoint behavior from the table | Branch on ad-hoc conditions |

## Common mistakes

- **Two sources of truth** (YAML plus a hard-coded enum) that drift.
- **Exposing internal codes** like `DATABASE_UNAVAILABLE` to third parties.
- **Making every code public**, freezing your internal freedom.

## Checklist

- [ ] Is the taxonomy a single reviewable artifact?
- [ ] Do all services import it?
- [ ] Is the public/private split explicit?
- [ ] Does adding a category require touching only one file?

## Related

- [Classifying Errors in Code](./02-classifying-errors-in-code.md)
- [Chapter 4 Reference Cheat-Sheet](../05-reference/README.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
