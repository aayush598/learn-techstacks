# Chapter 6 — Reference

> Part III · Chapter 6 · Cheat sheet, decision tables, and glossary.

## Cheat sheet — the four layers

```text
┌──────────────────────────────────────────────────────────────┐
│ 1 IDENTITY    code · name · category · severity · retryable    │  stable: route on this
│ 2 EXPLANATION message · details                                │  human / client facing
│ 3 CAUSALITY   cause · chain (bounded)                          │  diagnostics only
│ 4 CONTEXT     metadata · correlationId · operation · timestamp │  per occurrence, safe
└──────────────────────────────────────────────────────────────┘
```

## Cheat sheet — field checklist

| Field | Required | Client? | Purpose |
| ----- | -------- | ------- | ------- |
| `name` | Yes | No | Human/stack identification |
| `code` | Yes | Yes | Stable machine contract |
| `category` | Yes | Optional | Policy routing bucket |
| `severity` | Yes | No | Log level / alerting |
| `recoverable` | Yes | No | Continue vs abort |
| `retryable` | Yes | Yes | Retry eligibility |
| `message` | Yes | Public variant | Human diagnosis |
| `details` | No | Yes | Field-level validation |
| `metadata` | Yes | Allowlist | Safe structured context |
| `correlationId` | No | Yes | Cross-service tracing |
| `operation` | No | No | Which phase failed |
| `timestamp` | Yes | No | Ordering |
| `cause` | No | No | Original error |
| `stackTrace` | Yes | Never | Locating the fault |

## Decision table — category → defaults

| Category | Severity | Retryable | Recoverable | Typical HTTP |
| -------- | -------- | --------- | ----------- | ------------ |
| validation | info | no | yes | 422 |
| auth | warning | no | yes | 401/403 |
| business | info | no | yes | 409 |
| payment | warning | no | yes | 402 |
| database | error | yes | yes | 503 |
| external | warning | yes | yes | 502 |
| resource | warning | yes | yes | 429 |
| unexpected | error | no | no | 500 |

## Decision table — serialize or withhold?

| Field | Log JSON | Queue/DLQ | Client JSON |
| ----- | -------- | --------- | ----------- |
| code, category, retryable | ✅ | ✅ | ✅ |
| message | ✅ | ✅ | public variant |
| details | ✅ | ✅ | ✅ (safe fields) |
| metadata | ✅ | allowlist | allowlist subset |
| correlationId | ✅ | ✅ | ✅ |
| cause | summary | summary | ❌ |
| stackTrace | ✅ | ❌ | ❌ |

## Decision table — enrich or wrap?

| Situation | Action |
| --------- | ------ |
| Adding context (tenant, order) | Wrap with `cause` set to the original |
| Translating a vendor error to a code | Wrap, category `external`, preserve cause |
| Handling an expected business outcome | Construct a new `AppError`, no cause needed |
| Unknown native error | `toErrorObject()` → `INTERNAL_UNEXPECTED` |
| Adding to an aggregate | Collect with one marked `primary` |

## Message hygiene rules

```text
message := ONE_LINE ∧ NON_EMPTY ∧ SECRET_FREE ∧ NO_PII ∧ ≤ 2 KB
never   := parsed by code
never   := the user-facing string (derive that from code)
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Error model | The internal data structure every error is represented as |
| Identity layer | code, name, category, severity, retryable |
| Machine-readable code | Stable identifier handlers branch on |
| Correlation ID | Identifier shared across all errors of one operation |
| Request ID | Identifier for one inbound request |
| Cause | The original error a wrapper preserves |
| Causal chain | Ordered cause links from fault to representation |
| Field details | Structured array of per-field validation errors |
| Invariant | A property every error object must hold |
| Recoverable | Whether the caller can continue safely |
| Retryable | Whether retry plausibly helps |
| Safe metadata | Allowlisted, scalar, non-sensitive context |
| Schema version | Integer marking a non-additive serialized-shape change |

## Standard references (by name, no links)

- **RFC 9457** — Problem Details for HTTP APIs (external analogue).
- **RFC 6901** — JSON Pointer (field paths).
- **ES2022 `Error.cause`** — native cause preservation.
- **W3C Trace Context** — `traceparent` propagation.

## Signposts

- Error types and `Result` → [Ch. 7](../../07-error-classes-types-and-structured-results/README.md)
- Codes and registries → [Ch. 8](../../08-error-codes-and-error-registries/README.md)
- Redaction deep dive → [Ch. 36](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)

## Related

- [Chapter 6 Do's and Don'ts](../04-dos-and-donts/README.md)
- [The Complete Error Object Spec](../03-practical-examples/01-error-object-spec.md)
- [Chapter 6 Overview](../README.md)
