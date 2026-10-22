# Chapter 16 — Reference

> Part VI · Chapter 16 · Translation decision tree, boundary placement guide, mapping table, and glossary.

## Cheat sheet — the canonical shape

```text
AppError {
  code          stable, machine-readable        → clients, registry, logs
  category      VALIDATION|AUTH|CONFLICT|...     → HTTP mapping, dashboards
  transient     bool (default false)            → retry engine
  httpStatus    number                           → request boundary
  safeMessage   curated, no internals            → API response
  retryAfterMs  optional server hint             → backoff
  meta          allowlisted context              → logs/telemetry
  cause         ORIGINAL (server-side only)      → debugging
}
```

## Decision tree — translate or propagate?

```text
An error crosses a layer boundary.
│
├─ Is the representation changing (driver/vendor/framework → internal)?
│   ├─ Yes → TRANSLATE at this boundary:
│   │        1. extract the source code/class
│   │        2. map to stable code + category
│   │        3. set transient (default false) + retryAfterMs
│   │        4. attach the original as cause
│   │        5. derive safe details (allowlist / redact)
│   └─ No  → continue.
│
├─ Do I own the fallback/retry decision here?
│   ├─ No  → ENRICH (context) and PROPAGATE; do not change meaning
│   └─ Yes → continue.
│
└─ Is the format unknown?
    ├─ Yes → SAFE GENERIC (code=PROVIDER_ERROR, transient = status≥500), alert, keep cause
    └─ No  → apply the table mapping
```

## Boundary placement guide — where each translation belongs

| Translation | Boundary | Owner | Must not emit |
| ----------- | -------- | ----- | ------------- |
| native → application | request/job edge | boundary author | raw exception class |
| DB → domain | repository | repo maintainer | `SQLSTATE`, constraint, SQL |
| external → internal | integration adapter | adapter owner | vendor `type`/`code` |
| framework → application | framework adapter | app framework layer | framework exception |
| domain → transport | request boundary | transport layer | internals/stack/cause |
| worker → job failure | job boundary | worker | unhelpful `"failed"` |
| OS → application | adapter/edge | boundary author | raw `errno` |

## Decision table — normalize or keep distinct?

| Situation | Collapse? | Note |
| --------- | --------- | ---- |
| Two errors → different status/retry | ❌ | Keep distinct (`23505` vs `23503`) |
| Two errors → same consumer behavior | ✅ | One code + `details` |
| Field-level validation errors | ❌ collapse | One top-level code, per-field `details` |
| Unknown provider codes | ✅ | One generic code + alert |
| Two providers, same meaning | ✅ | Same stable code |
| Same code, different meaning | ❌ | Create a new code |

## Decision table — transient or permanent?

| Source code/status | Transient | Retry hint |
| ------------------ | --------- | ---------- |
| `40001`, `40P01` | Yes | backoff + jitter |
| `08006`, `08003`, `53300` | Yes | backoff |
| HTTP `429` | Yes | honor `Retry-After` |
| HTTP `503`, `504` | Yes | honor `Retry-After` if present |
| HTTP `500` from provider | Usually yes | backoff |
| HTTP `400`/`401`/`403`/`404`/`409`/`422` | No | — |
| `card_error` / business decline | No | — |
| `context_length_exceeded` | No | — |
| `ECONNRESET`/`ECONNREFUSED`/`ETIMEDOUT` | Yes | backoff |
| `ENOENT`/`EACCES` | No | — |

## Cheat sheet — preservation checklist

```text
For every translation, confirm:
  [ ] cause attached (native chaining)
  [ ] transient explicitly set (default false)
  [ ] retryAfterMs preserved when present
  [ ] field details preserved for validation
  [ ] requestId/tenantId carried in meta
  [ ] sensitive fields redacted from the cause copy
  [ ] chain depth ≤ 4 and acyclic
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Translation | Converting an error's representation at a boundary |
| Normalization | Reducing many formats into one internal shape |
| Stable code | Machine-readable code owned by you, not the vendor |
| Vendor code | Provider-specific identifier, adapter-only |
| Retry class | The transient/permanent classification carried by the error |
| Cause | The original wrapped error (server-side only) |
| Overgeneralization | Collapsing distinct errors into one vague code |
| Unknown branch | Safe default mapping for unrecognized formats |
| Circular chain | A `cause` cycle that loops renderers/serializers |
| Translation table | Declarative source→target mapping plus policy |

## Signposts

- Boundaries first → [Ch. 15](../../15-error-boundaries/README.md)
- Error model fields → [Ch. 6](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- Codes and registry → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- HTTP semantics → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- Contracts and versioning → [Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)

## Related

- [Chapter 16 Do's and Don'ts](../04-dos-and-donts/README.md)
- [SQLSTATE → Domain → HTTP map](../03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
- [Translation Decision Tree (Ch. 62)](../../../part-24-repeatable-blueprint/62-final-reference-materials/README.md)
