# Preventing Double Handling and Failures During Handling

> Part IV · Chapter 11 · Sections 11.14, 11.15 · _Estimated reading time: 19 min_
> **Prerequisite:** [Terminal State and the Standard Lifecycle](../01-concepts/05-terminal-state-and-standard-lifecycle.md)

## In one sentence

Double handling is detected with **markers, ledgers, and fault-injection tests**; failures inside
the handling machinery are contained by making every handler component **fail smaller, never
louder**, than the error it was meant to contain.

## Why this matters in production

These two stages protect the integrity of the whole lifecycle. When they fail, the damage is
unusual: you lose the *original* error (replaced by the handler's own crash), or you apply the
expensive action twice (retry, refund, DLQ write). Both produce incidents that are nearly
impossible to reconstruct after the fact — because the reconstruction machinery *is* the error
handler.

## Part A — Detecting and preventing double handling (11.14)

### The four duplication vectors

| Vector | Example | Detection |
| ------ | ------- | ---------- |
| **Two decision layers** | controller + service both retry | ledger review; attempt-marker |
| **Two entry points** | HTTP retry + queue redelivery re-run the saga | idempotency-key coverage; single side-effect test |
| **Two body writers** | filter + middleware serialize | `headersSent` guard; response-spy test |
| **Two translators** | repo + middleware both map `23505` | translation-point inventory (Ch. 9); code-shape test |

### Runtime net: the attempt marker

```ts
// decider is the only writer of `handled`
export function decideOnce(e: AppError, ctx: AttemptCtx): Decision {
  if (e.handled) {
    metrics.increment("lifecycle.double_decision", { code: e.code });
    throw new LifecycleViolation(`decision already made for ${e.code}`);
  }
  e.handled = true;
  return decide(e, ctx);          // pure policy after the guard
}
```

The marker travels *with* the error (it is an object field, not a log line), so any layer that
receives the same object instance can detect the second claim. For cross-process duplication
(HTTP + queue of the *same* logical operation), the marker cannot travel — use **idempotency
keys** and **operation records** instead: the second trigger observes the first's record and
collapses (Chapter 28).

### Verification net: fault-injection single-effect tests

```ts
test("one DB blip produces exactly one export side effect", async () => {
  const effects = spyOnS3Writes();
  failNextQueries("40001", { times: 1 });              // inject one transient failure
  await runExport(msg);                                 // via worker path
  await httpTriggerSameOperation(msg);                  // and via HTTP, same idempotency key
  expect(effects.count).toBe(1);                        // the lifecycle invariant, asserted
  expect(decisionsFor(msg.jobId)).toEqual(["retry", "success"]);  // exactly one decider acted
});
```

This test is the executable form of the ledger. Run it in CI for every money path.

## Part B — Failures during error handling (11.15)

### Why handlers fail

Error handling runs on the *worst* conditions: memory pressure (stack capture), disk/network
trouble (logging, DLQ), corrupted inputs (circular refs in serialization), and time pressure
(drain windows). Assume each component breaks:

| Component | Real failure mode | Containment pattern |
| --------- | ----------------- | ------------------- |
| serializer | circular `cause`, BigInt/Date edge cases, encoding errors | outermost try/catch -> minimal hard-coded body |
| redaction | pathological strings; regex DoS | allowlist first; match on keys, not content; bound work |
| logger | sink unavailable; synchronous fs blocking | async, fire-and-forget with local buffer; never throw |
| metrics | same as logger | never throw |
| compensation | provider down while primary is down | own retry budget; `COMPENSATION_FAILED` terminal + alert |
| DLQ publish | broker partition | capped retries; then **terminate process** (redelivery beats data loss) |
| `headersSent` write | streaming response | guard; abort stream; log |

### The containment ladder

```text
 level 0  the ORIGINAL error            (must reach logs + decision)
 level 1  primary handler (filter)      fails -> level 2
 level 2  minimal fallback body         fails -> level 3
 level 3  process boundary              log-to-stderr + exit non-zero (Ch. 9, 9.12)
```

Rules: each level is **strictly simpler** than the one above; each level **logs the level-0
code** even when it cannot render it; no level ever converts the situation into `2xx`.

```ts
export function safeProblem(e: AppError, reqId: string): ProblemDoc {
  try {
    return toProblem(e, reqId);
  } catch (serErr) {
    try { logger.error({ reqId, code: e.code, serErr }, "serializer failed"); } catch { /* level 3 */ }
    return { status: 500, type: "about:blank", title: "Internal error", statusText2: undefined,
             "request-id": reqId } as ProblemDoc;      // fixed, dumb, serializable
  }
}
```

### Compensation failures deserve special handling

Compensation is stage-10 work performed *because* the primary failed; its failure must never
replace the primary error silently. Sequence:

1. Primary error logged and recorded (terminal pending compensation).
2. Compensation attempted with its own budget (recommendation: 3 attempts).
3. If compensation exhausts its budget: terminal state `compensation_failed`, **alert a human**
   (this is a money/data-consistency event), keep both causes in the record.

## Key data / numbers

- Double-decision metrics worth shipping: `lifecycle.double_decision` (should be **0** in
  steady state; any non-zero value is a paging-worthy anomaly on money paths).
- Minimal fallback body: fixed fields only — `status: 500`, stable code, correlation ID.
- Compensation budget recommendation: **3** attempts with backoff, then human alert.
- DLQ-unavailable escalation: capped retry (**~3**), then process termination so the broker
  redelivers — losing the *handle* is safer than losing the *message*.
- Log-first ordering: the level-0 log line must be emitted before any serialization work
  (serializers are the least reliable part of the path under corruption).

## Real-world use case — Acme SaaS serializer crash

A `cause` chain formed a cycle (`e.cause = e2; e2.cause = e`) when a cache wrapper wrapped
itself on a retry. The JSON serializer threw `TypeError: Converting circular structure to JSON`
*inside* the global filter — Express's default handler then rendered
`<!DOCTYPE html>...Internal Server Error` **in HTML** to an API client expecting JSON. SDK
consumers parsed the HTML as JSON and threw *client-side*, producing a support storm that
looked like an SDK bug.

The fix had three parts, all from this file: (1) `safeProblem` with the minimal fallback;
(2) `normalize()` capped chain building with a visited-set to prevent cycles at creation time;
(3) a contract test serializing every registry code with adversarial causes. The same injected
cycle now produces a correct `500` JSON envelope with the correlation ID.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Markers + ledger + fault-injection tests (recommended) | Double handling fails loudly in CI | Test maintenance per money path | Default |
| Convention + review only | Zero runtime cost | Silent regressions under deadline pressure | Never for money paths |
| Trust handlers | Least code | One crash erases the original error | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Throw on a second decision claim | Silently ignore a duplicate decision |
| Keep fallbacks dumber than the handlers | Write a clever fallback serializer |
| Give compensation its own budget + alert | Let a refund failure vanish in a log |
| Terminate when the DLQ is unwritable | Ack messages you cannot park |

## Common mistakes

- **Marker on the class, not the instance** — a module-level `alreadyHandled` boolean "marks"
  every error; the marker must live on the error object.
- **Catching handler failures without logging the original** — you now have a new incident and
  no evidence of the old one.
- **Testing the happy path of the filter only** — inject a circular cause, a logger outage, and
  a `headersSent` stream; those are the realistic conditions.

## Checklist

- [ ] Deciders throw on double-claim; metrics alert on it.
- [ ] Every money path has a single-effect fault-injection test in CI.
- [ ] Serializer/redaction/DLQ writes have boring fallbacks; compensation has a budget + alert.
- [ ] The containment ladder (levels 0-3) is written in your architecture doc.

## Related

- [Terminal State and the Standard Lifecycle](../01-concepts/05-terminal-state-and-standard-lifecycle.md)
- [Finalization, Cleanup, and Terminal States](./02-finalization-cleanup-and-terminal-states.md)
- [Chapter 58 — Less Obvious Error-Handling Scenarios](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Chapter 51 — Correctness Properties](../../../part-20-correctness-and-validation/51-correctness-properties-of-error-handling/README.md)
