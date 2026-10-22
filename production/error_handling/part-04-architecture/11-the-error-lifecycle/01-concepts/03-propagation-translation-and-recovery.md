# Propagation, Translation, and Recovery

> Part IV · Chapter 11 · Sections 11.7–11.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [Enrichment and Cause Preservation](./02-enriching-and-preserving-cause.md)

## In one sentence

Stages 7–10 are the error's *active* half: it **propagates** up layers untouched, **translates**
at each boundary, gets **decided** by exactly one owner, and that owner **applies** retries or
compensation from an explicit budget.

## Why this matters in production

This is where lifecycles go wrong most often, because it is where money and side effects live:

- Propagation without translation leaks driver errors to clients (Ch. 9 leakage).
- Translation without cause preservation blinds triage (stage 6, previous file).
- A decision made in two layers multiplies retries (3 × 3 = 9 calls) and can double-charge.
- Retries without budgets never terminate; compensation without idempotency repeats side
  effects.

Stages 7–10 are Chapter 9's verbs in *time*: verbs describe what a layer may do; the lifecycle
reminds you they happen in order, exactly once for the decision.

## Stage 7 — Propagating across layers (11.7)

Default motion is **upward and untouched**: the error leaves the detecting layer and travels
toward the entry point. While propagating, a layer may:

- add context (stage 5), attach cause (stage 6) — *always allowed*;
- **not** change the outcome (that is stage 9's job);
- **not** re-represent it into a foreign vocabulary (that is stage 8's job at a boundary).

Async note: across promise chains, callbacks, and queue hops, propagation needs carriers — a
rejection must be awaited, a queue hop must copy `correlationId` and code into the message
(Chapter 12 covers the mechanics; the lifecycle rule is: **an error that cannot travel must be
finalized where it stands**, never dropped).

## Stage 8 — Translating at boundaries (11.8)

Each boundary crossing swaps vocabulary, once:

| Boundary | Translation | Preserved |
| -------- | ----------- | --------- |
| driver → repository | `23505` → `DUPLICATE_KEY` | `cause`, `retryable: false` |
| repository → application | persistence error → domain-meaning outcome | code, context |
| application → controller | outcome → HTTP status + envelope | code, correlation |
| application → worker | error → attempt record (code, retryable) | code, cause |
| service → service | internal → wire envelope (RFC 9457 + code) | code, status class |
| any → logs/DLQ | full chain, sanitized for secrets | everything except secrets |

Translation **must not** alter classification: a retryable error stays retryable unless a
documented policy says otherwise (e.g. a downstream service's `429` becomes the caller's
`503 class` but remains retryable).

## Stage 9 — Deciding recovery (11.9)

One owner, four canonical verdicts:

```text
            ┌── RETRY ──────── transient + idempotent + budget left ──▶ stage 10
 DECIDE ────┼── COMPENSATE ── prior steps completed; undo logically ──▶ stage 10
            ├── DEGRADE ───── optional feature; degraded result ──────▶ stage 11 (as success-with-flag)
            └── ABORT ──────── permanent / budget exhausted ──────────▶ stage 11 (as failure)
```

The decision inputs are exactly the classification fields from stage 4 plus attempt state:

| Input | Effect |
| ----- | ------ |
| `retryable: false` | abort (or compensate if prior steps exist) |
| `retryable: true` and budget left | retry |
| attempts exhausted | abort + finalize failed (DLQ for jobs) |
| prior steps with side effects | compensate before/instead of abort |
| feature optional + local fallback exists | degrade |

Decision ownership (Chapter 9): **application service** for request paths, **worker** for job
attempts, **saga owner** for multi-step compensation. Never the renderer, never the global
handler (Ch. 10).

## Stage 10 — Applying retries and compensation (11.10)

Execution of the verdict, with budgets and safety:

- **Retries:** bounded attempts (recommendation: 5), exponential backoff with jitter, honor
  `Retry-After` from the remote, total-deadline aware, and **only** for idempotent operations or
  operations made idempotent by keys/checkpoints (Chapter 28).
- **Compensation:** a *new* operation, not an undo-transaction — refunds, released reservations,
  deleted pending rows. Each compensation step must itself be **idempotent** and **failure-aware**
  (what if the refund also fails? → retry compensation, never skip silently; Chapter 39).
- **Budgets are part of the decision, not an afterthought:** attempts × delay ≤ operation
  deadline ≤ client/broker visibility timeout.

```ts
// stage 9 + 10 in one owner — Checkout saga
async function executeCheckout(cmd: CheckoutCmd) {
  const payment = await payments.reserve(cmd);                 // step 1 (side effect)
  try {
    await db.insertSubscription(cmd);                          // step 2
  } catch (err) {
    const e = normalize(err);
    if (isRetryable(e) && attempt < MAX) return retry();      // stage 9→10: RETRY
    await compensate(() => payments.release(payment.id));      // stage 9→10: COMPENSATE
    throw e;                                                   // continue lifecycle as failure
  }
}
```

## Key data / numbers

- Retry defaults worth writing down: max **5** attempts, backoff base **~2 s**, factor 2, full
  jitter; `Retry-After` respected when present (Chapters 27, 29).
- Idempotency prerequisites for safe retry: client idempotency key (Ch. 28), natural-key
  upserts, or deterministic resource keys (the `ExportJob` checkpoint pattern).
- Compensation is at-least-once: design each step idempotent; refunds/releases are usually
  naturally idempotent *given a payment/reservation ID*.
- Translation preservation rule: `retryable` and `correlationId` must survive every boundary —
  test them in the translation-point tests (Ch. 9 contracts).

## Real-world use case — Acme SaaS `Checkout`

During a Stripe degradation, one checkout executed: reserve payment (step 1 succeeded), insert
subscription (step 2 failed with `DB_UNAVAILABLE`). The old code retried step 2 three times
*inside the controller* while the queue-level retry re-ran the whole saga — three reservations,
one subscription, a support pile of "charged but no plan."

The lifecycle fix: stage 9 moved to the saga owner; `DB_UNAVAILABLE` (retryable, idempotent
insert) retried step 2 only, twice, with jitter; the final failure ran stage-10 compensation
exactly once (`release(payment.id)` — idempotent by ID); stage 11 rendered `503` +
`Retry-After`, stage 12 recorded `compensated`, and duplicate charges stopped. Same errors,
same code — only the stage ownership changed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Ordered stages with one decider (recommended) | No double retries; compensation is deliberate | Needs saga scaffolding for multi-step ops | Any operation with side effects |
| Retry wherever it fails | Fast to write | Amplification, duplicate side effects | Never for money paths |
| Compensate in the renderer | Appears "handled" | Renderer has no state; compensation lost | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Propagate untouched until the decision layer | Re-decide at every layer |
| Translate once per boundary; keep `retryable` | Change retryability silently in translation |
| Retry only idempotent steps, within budgets | Retry the whole saga for one failed step |
| Make compensation idempotent and failure-aware | Assume compensation always succeeds |

## Common mistakes

- **Retry before checking idempotency** — the first question of stage 9 is "may we run this
  again?", not "is it transient?".
- **Compensation as rollback** — cross-service steps cannot roll back; they compensate
  forward (Chapter 39).
- **Deadline blindness** — per-attempt retries ignoring the total deadline outlive the client's
  patience and the queue's visibility timeout; carry the deadline (Chapters 12, 29).

## Checklist

- [ ] Exactly one decider per operation, named in code and docs.
- [ ] Every translation point preserves `retryable` and correlation.
- [ ] Retry budgets (attempts, backoff, total deadline) are configured, not incidental.
- [ ] Multi-step operations have an ordered compensation plan with idempotent steps.

## Related

- [Enrichment and Cause Preservation](./02-enriching-and-preserving-cause.md)
- [Response, Finalization, and Cleanup](./04-response-finalize-and-cleanup.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
