# Chapter 51 — Do's and Don'ts

> Part XX · Chapter 51 · All sections

A condensed rule set distilled from the 18 correctness properties. Use it as a review checklist.

## Determinism and completeness (51.1–51.4)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every operation a closed set of terminal outcomes | Return `null`/`undefined` for failures |
| Model `unknown` as a real outcome | Assume a timeout means "failed" |
| Give every catch one of: propagate, translate-and-propagate, recover-and-record | Log and continue |
| Classify once, at the origin | Re-derive the category in each layer |
| Classify by code or exception type | Classify by message text |
| Preserve `cause`, vendor code, and request ID | Replace the cause with a new string |
| Reconcile error counts against terminal records | Trust "we log every error" |

## Safety and resources (51.5–51.9)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Project outbound errors through an allowlist | Serialize the internal error object |
| Test that a canary secret never escapes | Trust a redaction helper you never tested |
| Bound attempts, deadline, and budget | `while (true)` retry loops |
| Retry only classified-transient errors | Retry 4xx and business errors |
| Acquire and release resources in the same scope | Acquire in one function, release in another |
| Make cleanup idempotent and time-bounded | Assume cleanup always completes |
| Assert post-failure invariants | Assume they still hold |
| Enforce uniqueness in the database | "Check then act" in application code |
| Treat a duplicate as a success | Rethrow the unique-violation error |

## Contracts, transformation, and predictability (51.10–51.12, 51.17–51.18)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Build every error body with one validated builder | Let each handler format its own shape |
| Keep unknown failures failing closed by default | Map unknown to `200` or to an empty list |
| Distinguish "empty" from "could not load" | Let a fallback return a plausible default |
| Bound fallback, translation, and cause depth | Let fallback A point back at A |
| Preserve code, cause, retryability, and context in translation | Wrap everything as "upstream error" |
| Write a failure policy for every dependency | Let timeouts emerge from library defaults |

## Concurrency, partiality, and cancellation (51.13–51.16)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep error state per operation | Use module-level error accumulators |
| Count cancelled items separately | Fold cancellations into "failed" |
| Report successes + failures == attempted | Mark a batch "done" with silent `continue` |
| Check cancellation before irreversible effects | Check cancellation only at the top of a loop |
| Check recovery preconditions and record a stop reason | Retry blindly, or silently skip recovery |

## The five classic violations

1. **The Silent Discard** — `try { work() } catch {}`. The failure exists only in the absence of an
   effect.
2. **The Success-Shaped Failure** — `200 { ok: false }`. Every client learns to ignore the status
   code.
3. **The Unbounded Loop** — retries without attempts, deadline, or budget.
4. **The Duplicate Effect** — check-then-act dedupe plus a retry that is not idempotent.
5. **The Quiet Partial** — a batch that reports `done` while rows were skipped.

## Evidence checklist

- [ ] Every property has a named oracle (test, invariant query, or structural guarantee).
- [ ] Error counts reconcile against terminal records — the difference is zero.
- [ ] Pool checked-out count returns to zero after every injected failure.
- [ ] Public error bodies are schema-validated in tests.
- [ ] Unknown failures are exercised by a test that asserts a safe outcome.
- [ ] Concurrent-duplicate tests exist for every money-moving operation.
- [ ] Cancellation is asserted to never produce a success.
- [ ] Translation is tested field-by-field for metadata preservation.

## Anti-patterns in the wild

1. **`catch (e) { return null; }`** — the caller cannot distinguish "no data" from "broken".
2. **A catch that re-wraps without `cause`** — the original stack and code are gone.
3. **A retry inside a retry** — 3 × 3 × 3 attempts with nobody owning the policy.
4. **A fallback chain with a cycle** — the failure becomes an infinite loop with extra steps.
5. **A unique violation treated as a crash** — the system that prevents duplicates reports them as
   outages.

## Related

- [Chapter 51 Reference](../05-reference/README.md)
- [Chapter 52 — Failure-Path Analysis](../../52-failure-path-analysis/README.md)
- [Error Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
