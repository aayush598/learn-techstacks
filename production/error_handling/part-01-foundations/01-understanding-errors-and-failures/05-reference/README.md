# Chapter 1 — Reference

> Part I · Chapter 1 · Cheat sheet, decision table, and glossary.

## Cheat sheet — the causal chain

```text
FAULT ──causes──▶ ERROR ──becomes──▶ FAILURE
(defect)          (bad state)        (visible effect)
fix:              detect:            contain:
tests, review,    assertions,        boundaries, fallbacks,
config checks     invariants         retries, contracts
```

**Exception** = a mechanism (throw / Result / error value), not a thing to fix.

## Cheat sheet — the twelve dimensions

| Dimension | Values | One-line policy |
| --------- | ------ | --------------- |
| Expected | expected / unexpected | Model vs generic catch |
| Recoverable | yes / no | Recover vs terminate |
| Transient | yes / no | Retry vs don't |
| Deterministic | yes / no | Fix+test vs isolate+timeout |
| Sync/Async | sync / async | Local catch vs observe completions |
| Locality | local / remote | Handle vs timeout+idempotency |
| Origin | operational / programming | Config fix vs code fix |
| Nature | business / technical | No alert vs may alert |
| Cause | user / system | Actionable vs apologetic |
| Extent | partial / complete | Compensate vs clean fail |
| Posture | fail-fast / fail-safe | Stop vs protect |
| Flow | propagate / contain | Boundary choice |

## Decision table — first reaction to a failure

| Observed | Most likely | First action |
| -------- | ----------- | ------------ |
| `429` / `503` from remote | Transient, remote | Retry with backoff + `Retry-After` |
| `400` / `422` on valid-looking input | Permanent, expected | Validate, return field errors |
| `401` suddenly everywhere | Operational, remote | Fail-safe; check credential/config |
| Timeout, unknown remote outcome | Ambiguous | Idempotency check before retry |
| `NaN`/`null` produced locally | Programming, deterministic | Fail-fast, fix fault |
| One item of a batch failed | Partial | Record per-item result; don't mark all failed |
| Card declined | Business, permanent | No retry, actionable message |

## Decision table — boundary or propagate?

| If the fallback is… | Then… |
| ------------------- | ----- |
| Meaningfully different from failing | Place a boundary + fallback here |
| "Just rethrow with more context" | Propagate; add context, don't catch to log |
| "Retry the same operation" | Boundary + retry policy (transient only) |
| "Return a safe default" | Contain here |
| Undefined | Do not invent one; let it propagate to the outermost handler |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Fault | The defect/cause |
| Error | The incorrect internal state |
| Failure | The externally visible deviation |
| Exception | A signaling mechanism for errors |
| Failure domain | Set of components sharing fate |
| Fault boundary | Deliberate line containing a failure |
| Blast radius | How far a failure spreads |
| Fail-fast | Stop immediately on error |
| Fail-safe | Continue in a protected safe mode |
| Partial failure | Some steps succeeded, some failed |

## Signposts

- Classification in practice → [Ch. 4 Taxonomy](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)
- Boundaries in depth → [Ch. 15 Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- Blast radius at scale → [Ch. 57 Under Load](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)

## Related

- [Chapter 1 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part I Index](../../README.md)
