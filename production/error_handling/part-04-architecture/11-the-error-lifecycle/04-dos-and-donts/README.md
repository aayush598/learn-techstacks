# Chapter 11 — Do's and Don'ts

> Part IV · Chapter 11 · All sections 11.1–11.17 · _Estimated reading time: 11 min_

## In one sentence

Every rule below exists to keep one error on **one path** — detected once, enriched once,
decided once, rendered once, finalized once, and cleaned up on every path, including the
failure path.

## The lifecycle rules

| # | Stage | ✅ Do | ❌ Don't |
| - | ----- | ----- | -------- |
| 1 | Origin (11.1) | Enumerate origin classes per operation in a failure inventory | Assume "the code just throws" covers them |
| 2 | Detect (11.2) | Detect at the earliest sound moment; assert invariants where stated | Let `NaN`, null, or a stale id travel to a dependency |
| 3 | Represent (11.3) | Convert driver/vendor errors at the boundary they enter | Let raw SDK, SQL, or framework objects cross the boundary |
| 4 | Classify (11.4) | Read category, `retryable`, and severity from the registry | Re-derive classification from message text or status alone |
| 5 | Enrich (11.5) | Add **allowlisted** fields: operation, tenant, resource, attempt | Spread `req`, `body`, `user`, or headers into context |
| 6 | Cause (11.6) | Attach `cause` on every wrap and translation | Rethrow a bare `new Error("failed")` |
| 7 | Propagate (11.7) | Move the error upward untouched until the decider | Re-decide, retry, or "fix" it in a pass-through layer |
| 8 | Translate (11.8) | Translate once per boundary and preserve `retryable` + correlation | Change retryability silently during translation |
| 9 | Decide (11.9) | Name **one** decider per operation and record the verdict | Decide in the renderer, middleware, or global handler |
| 10 | Apply (11.10) | Retry only idempotent steps inside explicit budgets | Retry the whole saga for one failed step |
| 11 | Render (11.11) | Use one body-writer: code + safe detail + correlation ID | Emit stacks, cause chains, SQL, or vendor payloads |
| 12 | Finalize (11.12) | Write a durable terminal record, before ack where possible | Leave `pending`/`running` with no deadline |
| 13 | Cleanup (11.13) | Clean up structurally, boundedly, and idempotently | Skip cleanup on the failure path |
| 14 | Double handling (11.14) | Set a `handled` marker at the decider; assert one side effect | Re-decide "just in case" in another layer |
| 15 | Handler failure (11.15) | Log the original first; fall back to a fixed minimal body | Let a serializer/logger crash erase the primary error |
| 16 | Terminal (11.16) | Enforce no transitions out of terminal in storage | Resurrect a terminal record to retry it |
| 17 | Replay | Create a **new** operation referencing the old record | Blind-replay an ambiguous charge or commit |
| 18 | Async hops | Carry code + correlation ID across queues, callbacks, and streams | Drop an error at a detached promise or event handler |
| 19 | Standard (11.17) | Reuse one lifecycle for HTTP, jobs, webhooks, CLIs, and agent runs | Invent a second lifecycle per entry point |

## Anti-pattern — double handling (11.14)

```ts
// ❌ two deciders: the service retries, then the worker retries the whole job
async function runExport(job: Job) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try { return await exportOnce(job); }                 // decider #1 (service)
    catch (e) { if (!isRetryable(e)) throw e; }
  }
}
// worker redelivery on failure re-runs runExport(), decider #2 (worker)
```

**Symptom:** 3 × 3 = 9 executions, duplicate S3 objects, and duplicate `failed` records with
different codes. The `Checkout` version charges the customer more than once.

**Fix:** one named decider (usually the worker for jobs, the application service for requests),
an `e.handled` marker that throws on a second claim, and a fault-injection test asserting
exactly one side effect per failure (Chapter 28 for cross-process duplicates).

## Anti-pattern — handling errors during handling (11.15)

```ts
// ❌ the handler replaces the primary error and can fail itself
catch (err) {
  const code = classifyByLookup(err.message);   // may throw on unknown text
  await audit.write({ err });                   // may fail during an outage
  throw new AppError(code);                     // primary `err` and its cause are gone
}
```

**Symptom:** clients see the handler's failure, not the original one; the error log contains a
lookup error while the real fault disappears. A circular `cause` in the serializer can turn a
JSON `500` into an HTML `500`.

**Fix:** log the original error before enrichment or serialization, wrap with `cause` rather than
replacing, and keep the fallback **dumber than the handler** — a fixed
`{"status":500,"code":"INTERNAL_ERROR","request-id":"…"}` body. Compensation gets its own budget
and a `compensation_failed` terminal state plus an alert.

## Anti-pattern — cleanup that masks the primary error (11.13)

```ts
// ❌ a throw from finally replaces the error already in flight
let result;
try { result = await chargeCustomer(cmd); }
finally { await db.close(); }        // throws -> CONNECTION_CLOSED replaces CARD_DECLINED
```

**Symptom:** the user sees a cleanup error, retry classification is now wrong, and the payment
failure is untraceable. A hung cleanup can also outlive the drain window and orphan the request.

**Fix:** give cleanup its own short timeout, catch its failure, attach it as **secondary** or
suppressed, and rethrow the primary. Treat "already released" as success (idempotent cleanup).
For `ExportJob`, the same rule applies to aborting multipart uploads and releasing leases.

## More anti-patterns in brief

- **Success-shaped failure** — returning `200 { received: true }` for a transient webhook write;
  the producer stops retrying and the event is lost.
- **Pending forever** — a non-terminal state with no lease or deadline is a defect, not a state.
- **Blind replay** — replaying a job whose commit outcome is unknown; read back first.
- **Cleanup as a substitute for finalization** — releasing resources without recording *why* the
  operation ended.
- **Handler sprawl** — retry, compensation, and rendering spread across three layers; the same
  failure behaves differently by entry point.

## Code-review questions

1. Which single owner decides recovery for this operation, and where is it in the diagram?
2. Is every translation attaching `cause`, and does the chain reach the origin?
3. Can any context field contain a secret, PII, or a raw request body?
4. What is the retry budget, total deadline, and idempotency guarantee for each retried step?
5. What terminal state does this failure reach, and what forces it there after a crash?
6. If the serializer, logger, or DLQ write fails, what is the smaller fallback?
7. Can a second entry point (HTTP, queue, cron, webhook redelivery) re-decide this error?
8. Is cleanup bounded, idempotent, and guaranteed to preserve the primary error?

## Chapter checklist

- [ ] Every operation has a named decider and a documented recovery verdict.
- [ ] Detection points convert to the standard error model immediately.
- [ ] Classification comes from the registry, never from message text.
- [ ] Enrichment uses an allowlist per error code; no whole-object dumps.
- [ ] Every wrap/translation preserves `cause`, `retryable`, and correlation ID.
- [ ] Renderers emit one envelope with code + safe detail + correlation ID.
- [ ] Every started operation has a path to a terminal record, including crash paths.
- [ ] Non-terminal states carry a lease or deadline; a sweeper forces terminal.
- [ ] Terminal states are enforced by storage and never reopened.
- [ ] Replay creates a new record that references the old one.
- [ ] Cleanup runs on failure, is bounded, idempotent, and primary-preserving.
- [ ] Serializer, redaction, logging, and DLQ writes have boring fallbacks.
- [ ] Money paths have a single-effect fault-injection test in CI.
- [ ] The lifecycle is written down once and adopted by every new entry point.

## Related

- [The Lifecycle: Origin Through Classification](../01-concepts/01-lifecycle-overview.md)
- [Double Handling and Failures During Handling](../02-deep-dive/01-double-handling-and-error-during-handling.md)
- [Finalization, Cleanup, and Terminal States](../02-deep-dive/02-finalization-cleanup-and-terminal-states.md)
- [Chapter 11 Reference](../05-reference/README.md)
