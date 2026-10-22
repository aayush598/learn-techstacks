# Chapter 1 — Do's and Don'ts

> Part I · Chapter 1 · All sections

A condensed rule set distilled from the chapter. Use it as a review checklist.

## Vocabulary

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Distinguish fault (cause), error (state), failure (effect) | Use "error" for all four terms |
| Treat exceptions as one signaling mechanism | Treat "exception" as a synonym for "error condition" |
| Fix faults, detect errors, contain failures | Wrap a fault in try/catch and continue |

## Classification

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify along all twelve dimensions before deciding | Decide policy from the error message text |
| Retry only transient failures | Retry permanent errors (400/404/401) |
| Exclude business errors from on-call alerts | Page a human for a declined card |
| Represent partial failures explicitly | Assume multi-step ops are atomic |
| Record classification on the error object | Re-derive it inconsistently per handler |

## Boundaries and blast radius

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Draw boundaries where fallback differs from propagation | try/catch every line |
| Isolate pools/workers per dependency and tenant | Share one pool across independent providers |
| Give optional features their own boundary + fallback | Put optional features on the critical path |
| Estimate blast radius for each dependency | Assume redundancy equals isolation |

## Discipline

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fail-fast on corruption risk; fail-safe for optional features | Apply one style everywhere |
| Keep failure paths defined and testable | Leave "impossible" paths undefined |
| Never silently swallow | `catch {}` |
| Make routine errors easy, unusual ones explicit | Treat every failure as exceptional |

## Anti-patterns in the wild

1. **The Silent Swallow** — `try { work() } catch {}`. Turns failures into mysteries.
2. **The Universal Retry** — retrying everything, including 400s, amplifying outages.
3. **The Blanket 500** — returning 500 for expected business outcomes (should be 4xx).
4. **The Leaky Error** — returning raw `err.stack` or SQL to the client.
5. **The One True Handler** — a single global handler deciding business policy it cannot know.
6. **The Fatal Optimist** — catching a partial failure and marking the whole operation "success".

## Chapter checklist

- [ ] We can label faults, errors, and failures distinctly in incident reviews.
- [ ] Every retry decision consults the transient/permanent classification.
- [ ] Business errors never page on-call.
- [ ] Optional features are isolated with fallbacks.
- [ ] No empty catch blocks exist in the codebase.
- [ ] Public errors contain no internal details.

## Related

- [Chapter 1 Reference](../05-reference/README.md)
- [Error Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
