# Risk-Based Policy Selection: Turning Blast Radius into Retry, Fallback, and Termination Rules

> Part XXII · Chapter 56 · Sections 56.18, 56.4, 56.5, 56.6 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 3 — Error-Handling Requirements for a SaaS Product](../../../part-01-foundations/03-error-handling-requirements-for-saas/README.md), [Chapter 51 — Correctness Properties](../../../part-20-correctness-and-validation/51-correctness-properties-of-error-handling/README.md)

## In one sentence

A **risk tier** assigned to each operation turns "should we retry?" into a table lookup, and
it is the only way to spend engineering effort proportional to the cost of being wrong.

## Why this matters in production

Most teams apply one recovery philosophy across the whole codebase: "retry transient errors,
fall back for optional features, fail otherwise". That works until the first incident where
the wrong policy applies to a money-moving operation.

Concretely, the three most common tiering failures:

1. **The ledger is tiered as "a database error".** A serialization failure in the invoice
   table gets retried 3× — fine — but the same retry policy is applied to a unique-constraint
   violation on the payment ledger, which retries forever and never succeeds.
2. **The AI feature is tiered as "a dependency".** The LLM provider's `429` is retried
   without a budget, so Acme's summary traffic becomes the thing that keeps the provider
   rate-limited.
3. **The export is tiered as "async, so nobody is watching".** A failing `ExportJob` sits in
   the queue for hours before anyone learns the customer's data never arrived.

Risk tiering fixes all three by making the tier an explicit property of the **operation**,
not of the error category.

## Core concept

### Assigning a tier

A tier is derived from **blast radius** and **reversibility**:

```text
  blast radius        irreversible side effect?
        │                        │
        ▼                        ▼
   ┌──────────────────────────────────────────────┐
   │  T0  cosmetic          no                    │
   │  T1  convenience       no                    │
   │  T2  workflow          yes, but compensable  │
   │  T3  financial         yes, compensable      │
   │  T4  integrity/security yes, NOT compensable │
   └──────────────────────────────────────────────┘
```

The two questions that decide the tier:

| Question | If yes | If no |
| -------- | ------ | ----- |
| Does a wrong outcome affect money, entitlement, contract, or stored data? | Tier ≥ T2 | Tier ≤ T1 |
| Can the effect be undone by a compensating action within 24 hours? | Tier ≤ T3 | Tier = T4 |
| Does a user see a *wrong number* (not a missing feature)? | Tier ≥ T3 | Tier ≤ T2 |
| Would recovery need human judgement to be correct? | Tier = T4 | Tier ≤ T3 |

### The derived policy table

Once a code has a tier, the policy is derived, not chosen:

| Tier | Retry | Fallback / degrade | Compensate | Terminate | Alert |
| ---- | ----- | ------------------ | ---------- | --------- | ----- |
| **T0** cosmetic | 0 (cache instead) | Yes, silently marked | n/a | No | None |
| **T1** convenience | ≤ 2, idempotent only | Yes, marked `degraded: true` | Rarely | No | Dashboard |
| **T2** workflow | ≤ 3, idempotent required | Yes, if the reduced answer is still true | Yes, in reverse order | No | Notify owner |
| **T3** financial | ≤ 3 **only with an idempotency key** | **No** — a degraded financial answer is a wrong answer | **Mandatory** | No | **Page** |
| **T4** integrity / security | **0** | **No** | **No** (hides the fault) | **Yes** (quarantine) | **Page + incident** |

> The single most important row is T3. A fallback in a financial path is not a "reduced
> answer"; it is a wrong answer presented as right. That is how a customer ends up with a
> subscription at the wrong price.

### The tier of an error is not the tier of its category

An error's category (`dependency`, `validation`, `conflict`) says *what kind* of failure it
is. The tier says *what it means in this operation*. The same category can carry different
tiers in different operations:

| Error code | Category | Tier in `Checkout` | Tier in `AgentRun` | Why |
| ----------- | -------- | ------------------- | ------------------ | ---- |
| `HTTP_503` | dependency | T3 (payment provider) | T1 (LLM provider) | Money vs cosmetics |
| `TIMEOUT` | dependency | T3 | T2 (tool write) | Idempotent vs not |
| `VALIDATION_FAILED` | validation | T2 (business rule) | T2 | Neither is retryable |
| `DB_UNIQUE_VIOLATION` | conflict | T3 (ledger) | T2 (idempotency key reuse) | Integrity vs benign |
| `RATE_LIMITED` | throttling | T3 | T1 | Same code, different consequence |

This is why the registry entry carries **both** `category` and `riskTier`, and why the tier
must be evaluated **per operation**, not stored only on the code.

> ⚠️ **Hazard.** Storing the tier only on the error code forces one tier on all operations
> that share the code — which means either everything becomes T3 (no fallbacks anywhere) or
> everything becomes T1 (payment failures get degraded silently).

### 56.4 — Degradation eligibility, decided by tier

Degradation is a **tier-gated** decision:

- Allowed for T0–T1: the feature is optional and the reduced output is still true.
- Allowed for T2 only if the reduced output is still true for the *user's* purposes.
- **Forbidden for T3–T4**: a degraded financial or integrity answer is worse than an error,
  because the caller stops looking.

The "still true" test, concretely:

| Operation | Degraded output | Still true? | Verdict |
| --------- | --------------- | ----------- | ------- |
| Project board without AI summaries | Board data, no summary card | Yes | Degrade |
| Invoice without tax | Subtotal shown as total | **No** | Fail fast |
| Export preview unavailable | "Preview unavailable, download still works" | Yes | Degrade |
| Usage counter approximate | Rounded counter | Depends | Marker required |
| Subscription status unknown | "Unknown" | Yes if marked | Degrade with `degraded: true` |

### 56.5 — Retry eligibility, decided by tier *and* by evidence

Tier sets the ceiling; three facts set the actual number:

1. **Transient?** (`503`, timeout, `40001`, deadlock) — else 0 attempts.
2. **Idempotent or idempotency-keyed?** — else 0 attempts for any write.
3. **Within the caller's remaining deadline?** — else 0 attempts.

```ts
export function maxAttemptsFor(op: OperationContext, entry: RegistryEntry): number {
  if (!entry.retryable) return 0;
  if (op.tier === "T4") return 0;
  if (op.tier === "T3" && !op.idempotent) return 0;
  const ceiling = TIER_CEILING[op.tier];                  // T0:1, T1:2, T2:3, T3:3
  const byDeadline = Math.max(0, Math.floor(op.remainingMs / op.backoffMs));
  return Math.min(ceiling, byDeadline);
}
```

### 56.6 — Compensation eligibility

Compensation applies when the effect **happened** and the effect is **undoable**. Tier decides
*whether* undoing is permitted:

- **T3**: compensate **mandatory** when the operation has a completed, compensable side
  effect and the workflow cannot complete.
- **T2**: compensate when a compensable step exists; otherwise fail the workflow and let the
  owner restart it.
- **T4**: **never** compensate automatically — compensating an integrity failure usually
  destroys the evidence. Quarantine and escalate.

The compensation order is always **reverse of the completed steps**, and every compensation
must itself be idempotent.

## How it works (mechanics)

### Wiring the tier into the registry and the call site

```ts
// Registry: code-level facts only.
export type RegistryEntry = {
  code: string;
  category: Category;
  httpStatus: number;
  retryable: boolean;          // is the *condition* transient?
  publicTitle: string;
  defaultRiskTier: RiskTier;   // the tier IF no operation overrides it
};

// Operation: the tier that actually applies here.
export type OperationContext = {
  operation: string;           // "checkout.capture"
  tier: RiskTier;              // resolved for this operation
  idempotent: boolean;         // does this call carry an idempotency key?
  remainingMs: number;
  correlationId: string;
};
```

```ts
// ✅ Resolve the tier per operation, then derive the policy.
export function resolveTier(op: OperationContext, entry: RegistryEntry): RiskTier {
  const override = TIER_OVERRIDES[`${op.operation}:${entry.code}`];
  if (override) return override;
  return entry.defaultRiskTier;
}
```

The overrides table is small and reviewable:

```ts
const TIER_OVERRIDES: Record<string, RiskTier> = {
  "checkout.capture:PROVIDER_UNAVAILABLE": "T3",
  "agent.summary:PROVIDER_RATE_LIMITED": "T1",
  "agent.tool.write:DB_SERIALIZATION_FAILURE": "T3",
  "export.write:S3_UNAVAILABLE": "T2",
};
```

### A tier-aware retry policy

```ts
export async function withTieredRetry<T>(
  ctx: OperationContext,
  entry: RegistryEntry,
  fn: (attempt: number) => Promise<T>,
): Promise<T> {
  const attempts = maxAttemptsFor(ctx, entry);

  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      return await fn(attempt);
    } catch (err) {
      const normalized = classify(err);                 // one classification, at the origin
      if (normalized.code !== entry.code) throw err;     // a different failure — do not retry
      if (attempt === attempts) throw err;               // exhausted: preserve the final failure

      const delay = backoffWithJitter(attempt, normalized.retryAfterSeconds);
      await sleep(Math.min(delay, ctx.remainingMs));
    }
  }

  throw new ExhaustedError(entry.code);   // never reached; kept for totality
}
```

Note the two guards that make this safe: **only the expected code is retried** (a
`VALIDATION_FAILED` inside a retry-wrapped provider call is not retried), and the **final
failure is preserved** rather than replaced by a generic "retries exhausted".

### Degradation with a mandatory marker

```ts
export type Degradable<T> =
  | { ok: true; value: T }
  | { ok: true; value: T; degraded: true; degradedReason: string }
  | { ok: false; error: AppError };

export async function degradeOn<T>(
  ctx: OperationContext,
  entry: RegistryEntry,
  fn: () => Promise<T>,
  fallback: T,
): Promise<Degradable<T>> {
  try {
    return { ok: true, value: await fn() };
  } catch (err) {
    const normalized = classify(err);
    if (normalized.code !== entry.code) throw err;       // unexpected → propagate
    if (!DEGRADE_ALLOWED[ctx.tier]) throw err;           // T3/T4 → fail fast
    if (!entry.degradeAllowed) throw err;
    return { ok: true, value: fallback, degraded: true, degradedReason: normalized.code };
  }
}

const DEGRADE_ALLOWED: Record<RiskTier, boolean> = {
  T0: true, T1: true, T2: true, T3: false, T4: false,
};
```

## Worked example — `Checkout` (Acme SaaS), tier by tier

| Operation | Tier | Retry | Degrade | Compensate | Alert |
| --------- | ---- | ----- | ------- | ---------- | ----- |
| Validate the request | T2 | 0 | No (`422` is the answer) | n/a | None |
| Reserve a seat | T2 | 2 (idempotent reservation) | No — a checkout without a seat is wrong | Release the seat | Notify |
| Charge the card | **T3** | 3 **only with** `Idempotency-Key` | **No** | Refund if activation fails | **Page** |
| Activate the subscription | **T3** | 3 (idempotent upsert) | **No** | n/a (compensated by the caller) | **Page** |
| Send the receipt email | T1 | 2 | Yes — skip the email, mark queued | n/a | Dashboard |
| Update the audit log | **T4** | 0 | **No** | **No** | **Page + incident** |

The audit-log row is the one that surprises people. Appending to the audit log is T4 because a
missing audit entry is a *trust* failure, not a convenience failure: it cannot be
compensated (the missing record is gone), and silently continuing would hide it. Acme's
policy for `AUDIT_APPEND_FAILED` is to **fail the request** with `500` and to raise an
integrity incident — even though the business transaction already succeeded and must not be
rolled back.

This produces a subtle but important distinction:

```text
  The business effect is committed.        → do NOT compensate the business data.
  The audit append failed.                 → do NOT pretend the record was written.
  Both are true simultaneously.            → respond 500, alert, reconcile later.
```

Compensating the subscription here would refund a customer for a service they are using,
because a logging append failed. Tiers prevent that mistake automatically.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Risk tiers | 5 (T0–T4) | One per operation, not per code |
| Max retry attempts by tier | T0:0, T1:2, T2:3, T3:3 (idempotent only), T4:0 | Derived from the ceiling table |
| Retry-After honored for provider `429` | up to 60 s | Cap locally; do not obey blindly |
| Minimum `Retry-After` you emit | 1 s | Sub-second retries are a storm |
| Degradation allowed | T0–T2 only, and only if the reduced answer stays true | T3–T4 never |
| Compensation window | 24 h | Beyond that, manual review |
| Compensation order | Reverse of completed steps | Each step idempotent |
| Tier resolution | Per operation + code pair | Not per code alone |
| Operations to classify at Acme startup | ~12 | Payment, seat, subscription, email, audit, export, webhook, agent, upload, search, notification, report |
| Page on | T3 and T4 | T2 notifies; T1 dashboards |
| Error budget burn rate that triggers a freeze on new deploys | > 2× over 6 h (multi-window: 14.4×/1 h **and** 6×/6 h) | Stop shipping during an incident |

## Real-world use case — `ExportJob` (Acme SaaS)

`ExportJob` is asynchronous, which is exactly where tiering is most often skipped ("it's
background, who cares"). Acme's tiers:

| Step | Tier | Why |
| ---- | ---- | --- |
| Snapshot rows from Postgres | T2 | Read-only; a failed snapshot is retried |
| Generate the CSV in memory | T2 | Pure computation; retried |
| Upload to S3 | T2 | Idempotent (deterministic object key) |
| Write the "job complete" record | **T3** | It is the customer-visible state; a wrong record is wrong |
| Delete the tenant's earlier exports | T1 | Convenience; old exports can stay |

The T3 row changed the design. Because the completion record is the customer-visible truth,
Acme made the record write **idempotent** (`upsert` on `jobId`) and **retryable with an
idempotency key**, so a transient DB failure at the very end of a 40-minute export does not
lose 40 minutes of work.

The T1 row prevented an expensive mistake: the old code deleted the previous export *before*
writing the new completion record. If the record write failed, the customer had a new CSV in
S3 and no way to find it, and the old export was already deleted. Tiering said: keep the old
export, write the new record, then delete the old one — and if the delete fails, leave it
(a stale file is a T1 nuisance; a missing file is a T2 workflow failure).

Measured outcome: `ExportJob` completion records went from 0.6% missing to 0%, and
"customer says the export never arrived" tickets dropped 94% over one quarter.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One policy for all errors | Simple | Wrong effort allocation; money treated like cosmetics | Never |
| Category-based policy | Easy to write | Ignores per-operation consequence | Legacy systems only |
| **Risk-tier-based policy** | Effort follows blast radius | Requires classifying every operation | **Default** |
| Tier by code only | One place to look | Wrong tier when the code is reused across tiers | Small codebases only |
| Tier by operation + code | Correct per use case | Two-key lookup | **Default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign the tier to the **operation** | Assign the tier only to the error code |
| Degrade only when the reduced answer is still true | Degrade a financial total |
| Require an idempotency key before retrying a T3 write | Retry a T3 write because it "usually works" |
| Compensate T3 side effects in reverse order | Continue after a completed effect without compensation |
| Never compensate a T4 failure | "Clean up" an integrity failure automatically |
| Derive retry counts from the tier | Hand-write `attempts: 5` at call sites |
| Page on T3/T4, notify on T2 | Page on every error, including T0/T1 |

## Common mistakes

- **Tiering the category instead of the operation.** "A dependency error is T2" is how a
  payment-provider outage ends up silently degraded.
- **Letting the fallback be written by the caller.** If each caller picks its own fallback,
  the T3 rule ("no fallback") is enforced nowhere.
- **Compensating T4.** Refunding or rolling back after an integrity failure destroys the
  evidence you need to diagnose it.
- **Retrying a non-idempotent T3 write.** No idempotency key ⇒ no retry, regardless of tier.
- **Writing the tier but never using it.** A tier column nobody reads is documentation, not
  policy.
- **Using tiers to avoid alerting.** Downgrading a T3 to T2 to quiet a noisy alert is how a
  payment incident becomes a customer complaint.

## Checklist

- [ ] Every operation has a tier, and every code has a default tier.
- [ ] Tier overrides are keyed by operation + code and live in one reviewable table.
- [ ] Retry counts are derived from the tier, the idempotency flag, and the deadline.
- [ ] T3 writes carry an idempotency key before any retry is allowed.
- [ ] Degradation is gated on tier *and* on the reduced answer still being true.
- [ ] Compensation is mandatory for completed T3 side effects and runs in reverse order.
- [ ] T4 failures are never auto-recovered or compensated; they quarantine and alert.
- [ ] Alert routing matches the tier (dashboard → notify → page → incident).

## Related

- [Recovery Policy Trade-offs (56.4, 56.5, 56.6, 56.15, 56.16)](../01-concepts/03-recovery-policy-tradeoffs.md)
- [Fidelity and Risk (56.8, 56.13, 56.17, 56.18)](../01-concepts/04-fidelity-and-risk.md)
- [Checkout Decision Walkthrough](../03-practical-examples/01-checkout-decision-walkthrough.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
