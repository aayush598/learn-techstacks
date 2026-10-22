# Chapter 15 — Reference

> Part VI · Chapter 15 · Boundary placement guide, decision tree, and glossary.

## Cheat sheet — the boundary levels

| Level | Unit | Typical mechanism | Owner decides |
| ----- | ---- | ----------------- | ------------- |
| Function | one function | `try/catch`, `Result` | absorb one owned error |
| Module | package/repository | translate at edge | module error vocabulary |
| Domain | invariant/rule | typed throw / `Result` | business outcome |
| Request | one HTTP/gRPC call | middleware/exception filter | status + body |
| Transaction | one unit of work | `BEGIN…COMMIT` | commit/rollback/compensate |
| Job | one message/task | worker wrapper | retry/DLQ/done |
| Process | one instance | `uncaughtException` hook | shutdown/exit |
| Service | one service | protocol mapping | internal → protocol |
| Integration | one dependency | adapter | translate + degrade |
| UI | subtree/route | error boundary | fallback + recovery |

## Decision tree — should I place a boundary here?

```text
An error can occur at line L.
│
├─ Is the fallback at L meaningfully different from just failing?
│   ├─ No  → do NOT catch. Enrich (add context) and PROPAGATE.
│   └─ Yes → continue.
│
├─ Do I own the context needed to decide the fallback at L?
│   ├─ No  → do NOT catch. PROPAGATE to the layer that owns it.
│   └─ Yes → continue.
│
├─ Is L a translation point (driver/vendor/framework format ends here)?
│   ├─ Yes → translate to the internal model; preserve cause + retry class.
│   └─ No  → keep the representation, only contain/decide.
│
└─ Does absorbing here risk hiding a failure an outer layer needs?
    ├─ Yes → do NOT swallow; enrich + propagate (or rethrow typed).
    └─ No  → contain with an explicit, logged, honest fallback.
```

## Decision table — isolate or propagate?

| Failure | Required? | Fallback exists? | Action |
| ------- | --------- | ---------------- | ------ |
| Payment capture | Required | No safe substitute | Propagate → request boundary returns `402`/`503` |
| LLM summary | Optional | Placeholder | Isolate → `null`, log degradation |
| Recommendations | Optional | Empty list | Isolate → empty, log degradation |
| Cache read | Optional | Go to DB | Isolate → fall through to source |
| Billing read | Required | None | Propagate → `503` + `Retry-After` |
| Audit write | Required | None (compliance) | Propagate → fail operation |
| Email send | Required-but-deferrable | Queue for later | Isolate → queue, return degraded success |
| Analytics event | Optional/fire-and-forget | Drop | Isolate → drop, count metric |

## Decision table — which owner sets the HTTP status?

| Outcome | Owner | Status |
| ------- | ----- | ------ |
| Validation failure | Request boundary | 400/422 |
| Auth missing/invalid | Request (authn) | 401 |
| Permission/tenant | Request (authz) | 403 (or 404 to hide existence) |
| Resource missing | Domain → Request | 404 |
| Conflict/duplicate | Domain → Request | 409 |
| Rate limited | Request/middleware | 429 + `Retry-After` |
| Upstream transient failure | Request boundary | 503 + `Retry-After` |
| Unexpected/unknown | Request boundary | 500 (sanitized) |

## Cheat sheet — leakage channels and fixes

| Channel | Leak | Fix |
| ------- | ---- | --- |
| Response body | `res.json(err)` | Serialize an allowlisted Problem Details projection |
| Log | tokens, PII, headers | Redact; log `requestId` + safe context |
| `cause` chain | driver/vendor error re-serialized | Keep cause server-side only |
| Message | SQL, path, token in text | Stable `code` + curated `safeMessage` |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Error boundary | Deliberate line where errors are caught/translated/contained |
| Blast radius | Extent of impact when a component fails |
| Owner | The single layer accountable for a boundary's terminal decision |
| Granularity | Scope protected by one boundary |
| Fallback | Substitute outcome used when propagating is not chosen |
| Isolation | Containing a failure locally |
| Propagation | Letting an error travel to its owner |
| Failure→success conversion | Anti-pattern that hides a failure as success |
| Leakage | Internal/vendor/secret detail crossing a boundary |
| Terminal state | The defined end state of a unit of work |

## Signposts

- Translation at boundaries → [Ch. 16](../../16-error-translation-and-normalization/README.md)
- Global vs local handlers → [Ch. 10](../../../part-04-architecture/10-centralized-and-distributed-error-handling/README.md)
- Bulkheads/blast radius → [Ch. 29](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- UI boundaries → [Ch. 37](../../../part-14-frontend-and-full-stack/37-frontend-error-handling/README.md)

## Related

- [Chapter 15 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 15 — Runtime Boundaries](../01-concepts/03-runtime-boundaries.md)
- [Boundary Placement Guide (Ch. 62)](../../../part-24-repeatable-blueprint/62-final-reference-materials/README.md)
