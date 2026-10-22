# Chapter 15 — Do's and Don'ts

> Part VI · Chapter 15 · All sections

A condensed rule set distilled from the chapter. Use it as a boundary review checklist.

## Definition and necessity

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Place a boundary where fallback differs from propagating | Wrap every line in `try/catch` |
| Make each boundary contain, translate, or decide | Add a `catch` that does none of the three |
| Treat boundaries as architecture, not keywords | Assume a `try/catch` is automatically a boundary |
| Prevent leakage at every boundary | Trust that "no one will log the wrong object" |

## Levels and placement

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate DB/vendor errors at the repository/integration boundary | Let driver/vendor types reach the domain |
| Set HTTP statuses only at the request boundary | Scatter `res.status(...)` across services |
| Give every transaction a rollback path | Commit after swallowing an inner failure |
| Give every job a terminal state (success/retry/DLQ) | Let one poison job stall the worker loop |
| Fail-fast at the process boundary | Continue after an uncaught exception |

## Ownership and granularity

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign exactly one owner per boundary | Let two layers both "handle" an error |
| Right-size to the smallest distinct fallback | One global handler for all failures |
| Isolate optional work; propagate required work | Put optional dependencies on the critical path |
| Enforce ownership via structure + CI | Rely on comments and memory |

## Fallback behavior

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make fallbacks explicit, honest, and logged | Return plausible-but-wrong defaults |
| Escalate when the fallback itself fails | Loop on a failing fallback |
| Communicate degradation (stale, queued, reduced) | Silently change semantics |
| Mark failure as failure | Convert a failure into a silent success |

## Nesting and leakage

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Let inner boundaries absorb only what they own | Swallow at an inner layer what an outer owns |
| Enrich with the original as `cause` | Discard the cause or serialize it outward |
| Retry at exactly one nesting level | Retry at every level (amplification) |
| Serialize an allowlisted projection | `res.json(err)` / `JSON.stringify(err)` |
| Redact secrets/PII in logs | Log auth headers, tokens, card data |

## Anti-patterns in the wild

1. **The Rethrow Theater** — `catch (e) { log(e); throw e; }` at every layer: logs tripled, no
   decision made.
2. **The Universal Handler** — one global handler guessing business policy it cannot know.
3. **The Leaky Repository** — driver errors escaping into the domain and API.
4. **The Optimistic Inner Catch** — turning a failed write into `null`/success.
5. **The Optional-on-Critical-Path** — an LLM/recommendation timeout 500-ing the whole page.
6. **The Double Retry** — integration and job boundaries both retrying, multiplying load.
7. **The Cause Serializer** — `JSON.stringify` walking `.cause` and re-leaking everything.

## Chapter checklist

- [ ] Every boundary does at least one of contain / translate / decide.
- [ ] Each boundary has exactly one owner with a named decision.
- [ ] No driver/vendor type escapes its translation layer.
- [ ] No `catch` converts failure into silent success.
- [ ] Responses serialize an allowlist; causes never cross the network.
- [ ] Optional work is isolated; required work propagates.
- [ ] Retries are owned at exactly one level.

## Related

- [Chapter 15 Reference](../05-reference/README.md)
- [Chapter 15 — Runtime Boundaries](../01-concepts/03-runtime-boundaries.md)
- [Part XVII — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
