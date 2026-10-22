# Recovery Policy Trade-offs: Fail-Fast vs Degradation, Retry vs Failure, Retry vs Compensation

> Part XXII · Chapter 56 · Sections 56.4, 56.5, 56.6, 56.15, 56.16 · _Estimated reading time: 24 min_
> **Prerequisite:** [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md), [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)

## In one sentence

Recovery is not one decision but five, and the correct answers differ per operation: **fail fast
or degrade**, **retry or fail now**, **retry or compensate**, **recover now or defer**, and
**recover locally or terminate**.

## Why this matters in production

The single most expensive error-handling mistake is treating recovery as a single choice. A
team that retries everything gets a duplicate charge; a team that fails fast on everything
turns a degraded feature into an outage; a team that compensates when it should retry throws
away a completed payment.

Each of the five decisions has a specific failure mode when you get it wrong:

| Wrong choice | Consequence |
| ------------ | ----------- |
| Retry when you should compensate | **Double charge.** The first attempt succeeded; the response timed out. |
| Compensate when you should retry | **Lost work.** A transient DB error triggered a refund of a successful order. |
| Degrade when you should fail fast | **Silently wrong data.** A stale invoice shown as current. |
| Fail fast when you should degrade | **Unnecessary outage.** The LLM summary breaks the whole dashboard. |
| Defer recovery when the user is waiting | **The request times out anyway**, but now with a dangling job. |
| Recover locally when the process is corrupt | **Zombie state.** The worker keeps writing with a broken invariant. |

## Core concept

### 56.4 — Fail-fast vs degradation

| | Fail fast | Degrade |
| - | ---------- | ------- |
| Behaviour | Abort the operation immediately | Continue with reduced correctness or scope |
| Right when | Continuing would corrupt data, mislead the user, or breach an invariant | The feature is optional and the reduced answer is still useful |
| Cost of being wrong | Lost work, wrong data | A wrong answer presented as right |
| Signal | `500`/`409`/`422` with a stable code | `200` + a `degraded` marker, or `206 Partial Content`-style metadata |

The decisive question is: **is a reduced answer still a true answer?**

- Acme's project board shows tasks. If the AI "summarize" feature fails, showing the board
  without summaries is a *true* answer → **degrade**.
- Acme's invoice total is computed from line items. If the tax service is down and you show the
  invoice without tax, that is a **false** answer → **fail fast**.

The failure mode to design against is **silent inaccuracy**: degrading without a marker. If you
degrade, the response must say so — a `degraded: true` field, a `Warning` header, or a
distinct code — so the UI can display it and operators can count it.

### 56.5 — Retry vs immediate failure

Retry only when **all three** hold:

1. The failure is **transient** (a timeout, `503`, a deadlock, `40001` serialization failure).
2. The operation is **idempotent**, or carries an idempotency key.
3. The **time budget** allows it (the caller's deadline has room for the retries).

The failure mode to design against is **retrying a permanent failure**, which is the most
common cause of a retry storm (Chapter 57). A `422` validation error retried 3 times is 3× the
load for 0% success probability.

### 56.6 — Retry vs compensation

This is the most dangerous pair in the chapter, because the two are often confused.

```text
  DID THE SIDE EFFECT HAPPEN?
        │
        ├── NO  (failed before the effect)  ──▶ RETRY
        │        e.g. connection refused, DNS failure, validation rejected
        │
        ├── UNKNOWN (timeout, connection reset after write) ──▶ IDEMPOTENCY KEY + STATUS CHECK
        │        e.g. read timeout after the provider committed the charge
        │
        └── YES (the effect happened)      ──▶ COMPENSATE
                 e.g. Stripe returned a charge ID, then activation failed
```

- **Retry** re-attempts the *same* operation because it did not take effect.
- **Compensation** performs a *different* operation that logically undoes a completed one
  (refund, release reservation, deactivate entitlement).

The question is not "is it recoverable" — it is **"has the effect already happened?"**

### 56.15 — Sync vs deferred recovery

Some failures must be handled before the caller gets an answer; some can be handed to a worker.

| | Synchronous recovery | Deferred recovery |
| - | --------------------- | ------------------- |
| Caller waits | Yes | No |
| Use for | Operations the user is waiting on (checkout, upload, export start) | Long or slow operations (export run, email, report) |
| Implementation | Inline retry, inline compensation | Enqueue a job with a `compensation`/`retry` instruction |
| Risk | Latency budget consumed | The user gets "accepted" and the outcome arrives later |

The test: **is the caller blocked on the outcome?** If yes, the recovery must be synchronous or
the caller must be told to expect it later. Deferring a checkout failure to a background job
means the user sees "success" for a payment that failed.

### 56.16 — Local recovery vs termination

Most failures should be recovered locally: the operation fails, the boundary converts it to a
response, the process keeps running. But some failures are not recoverable by the process:

| Condition | Action |
| -------- | ------ |
| Invariant violated and the process holds derived state | **Terminate** — restart from a known state |
| Memory corruption / OOM / heap exhaustion | **Terminate** — the process is not trustworthy |
| Deserialization of an internal state file failed | **Terminate** — do not run with a half-read state |
| Config missing at startup | **Terminate** at boot, not at first use |
| A single request failed | **Recover locally** — return an error response |
| A single job failed | **Recover locally** — retry, then DLQ |

The rule: **terminate when continuing risks corruption; recover when continuing is safe.**

> ⚠️ **Hazard.** "Recover locally" includes the dangerous variant where the process continues
> after an invariant violation. If Acme's worker detects that the export checkpoint and the
> S3 object disagree, continuing means writing more rows from a bad offset. Terminate the
> worker and let the orchestrator restart it.

## How it works (mechanics)

### The recovery decision, encoded

```ts
// ✅ One function per operation, answering all five questions explicitly.
export type RecoveryPlan =
  | { action: "fail"; code: string }
  | { action: "degrade"; reason: string; degradedValue: unknown }
  | { action: "retry"; attempts: number; backoffMs: number }
  | { action: "compensate"; steps: string[] }
  | { action: "defer"; jobType: string; delaySeconds: number }
  | { action: "terminate"; reason: string };
```

The classification of an error into a plan is driven by the **registry**, not by scattered
conditionals:

```ts
const RECOVERY: Record<string, RecoveryPlan> = {
  PAYMENT_CARD_DECLINED:        { action: "fail", code: "PAYMENT_CARD_DECLINED" },
  PAYMENT_PROVIDER_UNAVAILABLE: { action: "retry", attempts: 3, backoffMs: 250 },
  SUBSCRIPTION_ACTIVATION_FAILED:{ action: "compensate", steps: ["refund", "release_seat"] },
  SUMMARY_MODEL_UNAVAILABLE:    { action: "degrade", reason: "llm_unavailable", degradedValue: null },
  DB_SERIALIZATION_FAILURE:     { action: "retry", attempts: 3, backoffMs: 100 },
  EXPORT_S3_WRITE_FAILED:       { action: "defer", jobType: "export.write", delaySeconds: 30 },
};
```

Now the question "retry or compensate?" has a single answer per code, and the answer is
reviewable in one table.

### Detecting "the effect happened" — the ambiguous case

The hardest case is "did it happen?". Two techniques handle it:

**Technique 1 — idempotency key.** Send a key so a retry collapses instead of duplicating.

```ts
// ✅ The provider returns the same result for the same key.
const result = await stripe.charges.create(
  { amount: 4999, currency: "usd", source: token },
  { idempotencyKey: `checkout:${checkoutId}` },
);
// A retry with the same key returns the ORIGINAL charge, not a second one.
```

**Technique 2 — status check.** Before retrying an ambiguous write, ask the provider what
happened.

```ts
// ✅ Timeout during charge → look it up before deciding.
async function chargeWithReconciliation(input: ChargeInput): Promise<ChargeOutcome> {
  const key = `checkout:${input.checkoutId}`;
  try {
    const charge = await stripe.charges.create(input.payload, { idempotencyKey: key });
    return { ok: true, chargeId: charge.id };
  } catch (err) {
    if (isAmbiguousTransport(err)) {
      const existing = await stripe.charges.list({ idempotencyKey: key });   // status check
      if (existing.data.length > 0) return { ok: true, chargeId: existing.data[0].id };
    }
    throw err;
  }
}
```

> The failure mode to avoid is "retry on timeout" for a **non-idempotent** write with no
> reconciliation. That is precisely how a customer is charged twice for one checkout.

### Fail-fast vs degrade in code

```ts
// ✅ Degrade with an explicit marker — never silently.
export type InvoiceView =
  | { total: number; tax: number; degraded: false }
  | { total: number; tax: null; degraded: true; degradedReason: "TAX_SERVICE_UNAVAILABLE" };

export async function renderInvoice(id: string): Promise<InvoiceView> {
  const invoice = await invoices.find(id);
  const tax = await taxService.compute(invoice.lineItems).catch((err) => {
    if (isTransient(err)) return null;      // degrade
    throw err;                               // fail fast on a real bug
  });

  if (tax === null) {
    // Degrading is only allowed because the total without tax is still marked.
    return { total: invoice.subtotal, tax: null, degraded: true,
             degradedReason: "TAX_SERVICE_UNAVAILABLE" };
  }
  return { total: invoice.subtotal + tax, tax, degraded: false };
}
```

Compare with the *illegal* version — degrade on any error:

```ts
// ❌ A real bug in tax computation now silently produces a wrong invoice.
const tax = await taxService.compute(invoice.lineItems).catch(() => 0);
```

## Worked example — `Checkout` (Acme SaaS)

Acme's `Checkout` runs three steps: **reserve seat → charge card → activate subscription**.

They wrote the policy by walking the five decisions:

| Step | Decision | Rationale |
| ---- | -------- | --------- |
| Reserve seat | 56.4 **fail fast** | Continuing without a seat means charging for something unavailable |
| Charge card | 56.5 **retry** (idempotent) | Provider outage is transient; `Idempotency-Key` makes retry safe |
| Charge card (declined) | 56.4 **fail fast** | The customer must act; a degraded checkout is a charge without a seat |
| Activate subscription | 56.6 **compensate** | The effect (a charge) already happened; undo it with a refund |
| Whole flow | 56.15 **sync** | The user is on the checkout page waiting for the outcome |

The compensation path, written out:

```ts
export async function startCheckout(input: CheckoutInput): Promise<CheckoutOutcome> {
  const seat = await seats.reserve(input.tenantId, input.planId);
  if (!seat.ok) return { ok: false, error: seat.error };            // fail fast: no seat

  const charge = await payments.charge(input, { idempotencyKey: `checkout:${input.checkoutId}` });
  if (!charge.ok) {
    await seats.release(seat.value.reservationId);                  // undo step 1
    return { ok: false, error: charge.error };                      // fail fast: declined
  }

  const activation = await subscriptions.activate(charge.value.chargeId);
  if (!activation.ok) {
    await payments.refund(charge.value.chargeId, { idempotencyKey: `refund:${charge.value.chargeId}` });
    await seats.release(seat.value.reservationId);                  // undo step 1
    return { ok: false, error: activation.error };                  // compensate
  }

  return { ok: true, subscriptionId: activation.value.subscriptionId };
}
```

Note the ordering: **compensations run in reverse** of the completed steps, and each
compensation is itself idempotent (the refund carries its own idempotency key, so a retry of
the compensation cannot double-refund).

What this avoids: the classic "the charge succeeded but activation failed, so the user paid
and has no access" support ticket, and the equally classic "the refund went out twice".

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Retry attempts, provider read/write | 3 | With exponential backoff and full jitter |
| Retry attempts, DB serialization failure (`40001`) | 3 | Within the caller's remaining deadline |
| Retry attempts, HTTP `503` from a dependency | 2–3 | Honor `Retry-After` when present |
| Retry attempts, `422` / `4xx` validation | **0** | Permanent — retrying is pure load |
| Max total retry time | ≤ 30 s or the caller deadline, whichever is smaller | A retry that outlives the deadline is wasted load |
| `Retry-After` minimum on a `429` | 1 s | Sub-second retries are a storm |
| `Retry-After` maximum honored from a server | 60 s | Longer values are capped locally, not obeyed blindly |
| Idempotency key TTL | 24 h | Matches Stripe's de-duplication window |
| Compensation window | 24 h for refunds | Beyond it, escalate to manual review |
| Degradation marker field | Required | `degraded: true` + a reason code |
| Process termination trigger | Invariant violation, OOM, corrupt state | Not for ordinary request failures |

## Real-world use case — `ExportJob` (Acme SaaS)

`ExportJob` generates a large CSV and uploads it to S3. Its failure modes split cleanly:

- **S3 returns `503 Slow Down`** → transient → **retry** with backoff (the job is idempotent
  because the object key is deterministic: `exports/{tenantId}/{jobId}.csv`).
- **The generator runs out of memory** → not transient, and not safe to retry in-process →
  **defer** to a worker with a bigger memory limit, and record the attempt.
- **The tenant's subscription expired mid-export** → permanent, business rule → **fail fast**
  with `EXPORT_SUBSCRIPTION_INACTIVE`, and delete the partial file so the tenant does not
  download a half-written CSV.
- **The upload succeeds but the "job complete" DB write fails** → the effect happened →
  **compensate** by deleting the S3 object, then re-run the job (the DB write is idempotent
  because it is an upsert keyed by `jobId`).

Acme's original implementation retried the *whole* job on any error, including the
subscription-expired case, which produced 40 identical failures per minute and a queue that
never drained. Splitting the policy by code reduced `ExportJob` failures from 2,300/month to
190/month, and the queue drain time from 6 hours to 11 minutes.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fail fast | Honest, cheap, prevents bad state | Loses optional functionality | Invariants, financial truth, required dependencies |
| Degrade | Preserves core UX | Silent inaccuracy if unmarked | Optional features with truthful reduced output |
| Retry | Absorbs transient faults | Amplifies load; duplicates side effects | Transient + idempotent + within deadline |
| Compensate | Restores consistency | Compensations can fail; not exact undo | The effect already happened |
| Defer | Keeps latency low | Outcome arrives later; caller must be told | Long operations, non-blocking work |
| Terminate | Guarantees a clean slate | Service interruption; possible loop | Corruption, OOM, invariant violation |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask **"has the effect happened?"** before choosing retry vs compensation | Retry because "it might work" |
| Use an idempotency key for every retryable write | Retry a non-idempotent write after a timeout |
| Mark every degraded response with `degraded: true` + a reason | Return a plausible-but-wrong value |
| Retry only transient errors, never `4xx` validation | Retry `422` because the client "will fix it" |
| Run compensations in reverse order of completed steps | Compensate in the order the steps ran |
| Make compensations idempotent | Assume a compensation ran exactly once |
| Terminate the process on corruption | Continue with a violated invariant |

## Common mistakes

- **Degrading on programming errors.** A `catch` around a computation that swallows a bug
  produces a wrong number that nobody notices for a month.
- **Retrying inside a compensation.** The compensation itself failed transiently and the
  retry logic re-ran the *original* operation.
- **Compensating without a check.** A refund is issued for a charge that was never created,
  because the timeout made the outcome unknown.
- **Deferring a user-facing operation.** The checkout returns `202 Accepted`, the user closes
  the tab, and the payment later fails.
- **Treating termination as a failure.** Restarting a corrupt worker is *recovery*, not an
  error. If the orchestrator treats the restart as a crash loop, it will page someone.

## Checklist

- [ ] Every operation has a written recovery plan per error code (fail / degrade / retry /
      compensate / defer / terminate).
- [ ] Retry is limited to transient + idempotent + within-deadline failures.
- [ ] Every retryable write carries an idempotency key.
- [ ] Ambiguous outcomes (timeouts) are reconciled before retrying.
- [ ] Every degraded response carries an explicit `degraded` marker.
- [ ] Compensations run in reverse order and are themselves idempotent.
- [ ] Termination triggers are enumerated and distinct from ordinary request failures.

## Related

- [Control-Flow Shape (56.1, 56.7, 56.14)](./01-control-flow-shape.md)
- [Fidelity and Risk (56.8, 56.13, 56.17, 56.18)](./04-fidelity-and-risk.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
