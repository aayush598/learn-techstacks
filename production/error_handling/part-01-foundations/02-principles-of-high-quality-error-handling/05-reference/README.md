# Chapter 2 — Reference

> Part I · Chapter 2 · Cheat sheet, decision tables, and chapter glossary.

## Cheat sheet — the 20 principles in one screen

| # | Principle | One-line rule |
| - | --------- | ------------- |
| 2.1 | Explicitness over implicit | State failure in the type/signature |
| 2.2 | Consistency | Same situation → same behavior, everywhere |
| 2.3 | Errors first-class | Owner + code + documented outcome |
| 2.4 | Separation of concerns | Domain names; boundaries decide |
| 2.5 | Central policy / local decisions | Rules central, choices local |
| 2.6 | Single responsibility | One job per handler |
| 2.7 | Fail-fast | Stop on bugs/invariants/critical deps |
| 2.8 | Fail-safe | Deny on security/integrity uncertainty |
| 2.9 | Graceful degradation | Honest reduced service for optional deps |
| 2.10 | Proportionate defense | Defend at boundaries, not every line |
| 2.11 | Least surprise | Behavior matches the name |
| 2.12 | Transparency vs abstraction | Abstract outward, preserve inward |
| 2.13 | Preserve cause | Attach `cause`/`%w`/`from exc` |
| 2.14 | No swallowing | Handle/translate/rethrow/record |
| 2.15 | No failure→success | Never return OK on failure |
| 2.16 | No redundant handling | Handle once, at the owner |
| 2.17 | No ceremonial rethrow | Catch only to add context |
| 2.18 | Predictable behavior | Caller knows retry/outcome |
| 2.19 | Minimize boilerplate | Shared primitives, not a framework |
| 2.20 | Optimize maintainability | Locate, change, and read easily |

## Decision table — which posture?

| Question | Answer | Posture |
| -------- | ------ | ------- |
| Security/integrity decision? | yes | **Fail-safe** (deny) |
| Programming/invariant error? | yes | **Fail-fast** |
| Recoverable + idempotent? | yes | **Retry**, then re-evaluate |
| Critical dependency down? | yes | **Fail-fast** at request (`503`) |
| Optional feature? | yes | **Degrade** (honest fallback) |
| Ambiguous remote outcome? | yes | **Idempotency check**, then retry |

## Decision table — catch, propagate, or contain?

| If the fallback is… | Then… |
| ------------------- | ----- |
| Meaningfully different from failing | Catch + fallback here |
| "Add context and rethrow" | Catch, attach `cause` |
| "Just rethrow" | Do not catch |
| "Record a metric and rethrow" | Catch, record, rethrow |
| Undefined | Propagate to the outer boundary |

## Decision table — where does handling live?

| Concern | Centralized | Local |
| ------- | ----------- | ----- |
| Native → app error mapping | ✅ registry | |
| Category → HTTP status | ✅ registry | |
| Retry eligibility | ✅ policy table | |
| Optional-feature fallback | | ✅ caller |
| Business rule violation | | ✅ domain |
| Logging format | ✅ shared | |

## Error outcome matrix (defaults)

| Error class | HTTP | Retryable | Posture |
| ----------- | ---- | --------- | ------- |
| Validation | `422` | No | Fail-fast (reject input) |
| Auth | `401` | No | Fail-safe (deny) |
| Authorization | `403` | No | Fail-safe (deny) |
| Not found | `404` | No | Fail-fast (outcome) |
| Conflict/duplicate | `409` | No (idempotent: `200`) | Outcome |
| Rate limited | `429` | Yes (`Retry-After`) | Retry |
| Upstream timeout | `504` | Yes | Retry / degrade |
| Dependency down | `503` | Yes | Fail-fast / degrade |
| Programming | `500` | No | Fail-fast + alert |

## Signal-erasure quick scan

```text
Look for:  catch {}            → swallow
           return ok in catch   → failure→success
           new Error("...")     → cause-drop
           catch (e){throw e}   → ceremonial
           3× log same error    → redundant handling
           null for 3 meanings  → implicit contract
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Explicit contract | Failure visible in type/signature/response |
| Policy | Central rule mapping error → behavior |
| Decision | Local, context-specific recovery choice |
| Posture | fail-fast / fail-safe / degrade per operation |
| Degradation | Honest reduced functionality |
| Signal erasure | Any step that destroys error evidence |
| Failure→success | Returning OK when the operation failed |
| Ceremonial rethrow | A catch that only rethrows, adding nothing |
| Boilerplate | Repetitive plumbing that hides flow and drifts |

## Signposts

- Posture in depth → [Ch. 29 Timeouts & Breakers](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md) · [Ch. 30 Degradation](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- Consistency as a contract → [Ch. 8 Codes](../../../part-03-error-models/08-error-codes-and-error-registries/README.md) · [Ch. 20 Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- Cause preservation → [Ch. 16 Translation](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- Anti-patterns → [Ch. 46 Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)

## Related

- [Chapter 2 — Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 2 — Chapter overview](../README.md)
- [Part I — Foundations](../../README.md)
- [Glossary](../../../GLOSSARY.md)
