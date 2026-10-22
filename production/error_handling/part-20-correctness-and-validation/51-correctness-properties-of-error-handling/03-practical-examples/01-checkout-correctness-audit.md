# Checkout Correctness Audit (51.1–51.18)

> Part XX · Chapter 51 · Practical example · _Estimated reading time: 24 min_
> **Prerequisite:** [Determinism and Completeness (51.1–51.4)](../01-concepts/01-determinism-and-completeness.md)

## In one sentence

A property-by-property audit of Acme SaaS's `Checkout` flow finds **eleven violations across nine
properties** — and shows the fix for each one, ordered by risk.

## Why this matters in production

Audits are how correctness becomes a practice rather than an aspiration. This audit is written the
way you would run it in a real repository: take the flow, walk it property by property, record the
verdict and the evidence, and rank the gaps by risk.

`Checkout` is the right subject: it is multi-step, it moves money, it spans a database and a
payment provider, and it has a webhook that updates the same state asynchronously.

## The flow under audit

```text
  POST /checkout
        │
   1. authenticate ─────────────► 401/403
        │
   2. validate request ──────────► 422 (field errors)
        │
   3. BEGIN; insert checkout_attempts (status='pending'); COMMIT
        │
   4. POST stripe.charges.create (Idempotency-Key: attempt.id)
        │
   5. BEGIN; insert subscriptions (status='active'); insert entitlements; COMMIT
        │
   6. insert outbox_events ('subscription.created')
        │
   7. COMMIT  → publish to queue
        │
   8. send receipt email
        │
   9. return 201 { checkoutId, subscriptionId }
```

## The audit

| # | Property | Observed behaviour | Verdict | Evidence |
| - | -------- | ------------------ | ------- | -------- |
| 51.1 | Defined outcome per failure path | `catch { return null }` in step 5 | ❌ Violated | `null` is not a declared outcome |
| 51.2 | Never silently discarded | Step 4's catch logged and returned `null` | ❌ Violated | No terminal record written on failure |
| 51.3 | Deterministic classification | Timeout classified `transient` in the adapter, `permanent` in the handler | ❌ Violated | Two `classify()` implementations |
| 51.4 | Causes recoverable | `new Error("Payment failed")` dropped `cause` and Stripe's request ID | ❌ Violated | Error object had no `cause` |
| 51.5 | No sensitive exposure | HTTP body included `err.stack` for `500`s | ❌ Violated | Stack in the response payload |
| 51.6 | Retries terminate | 3 attempts, no deadline, no budget, retried `400`s too | ❌ Violated | `withRetry` had `maxAttempts` only |
| 51.7 | Cleanup occurs | Connection released only on the success path | ❌ Violated | Manual `conn.release()` after the `try` |
| 51.8 | Consistency preserved | Charge succeeded, subscription insert failed → charged, no entitlement, no compensation | ❌ Violated | No state machine, no ledger |
| 51.9 | No duplicate side effects | No `Idempotency-Key` forwarded to Stripe | ❌ Violated | Two charges on retry |
| 51.10 | Responses follow contracts | `200 { ok: false }` on failure; `500` with a stack | ❌ Violated | Body shape differed per handler |
| 51.11 | Safe fallback for unknown | Unknown error → `null` → `200 { data: null }` | ❌ Violated | Unknown mapped to success |
| 51.12 | No unbounded recursion | 401 → refresh token → retry → 401 → refresh (no guard) | ❌ Violated | Refresh retry had no counter |
| 51.13 | Concurrency-safe | Dedupe check and insert were two statements | ❌ Violated | Redis `GET` then `SET` |
| 51.14 | Partial failures accurate | n/a (single-tenant flow) | ⚠️ Not applicable | — |
| 51.15 | Cancellation not success | Client disconnect during step 4 left the attempt `pending` | ❌ Violated | No `cancelled` outcome |
| 51.16 | Recovery preconditions | Retry ran after the request deadline; compensation had no precondition check | ❌ Violated | No `decideRecovery()` |
| 51.17 | Transformations preserve metadata | `DB_UNIQUE_VIOLATION` (SQLSTATE 23505) became generic `CONFLICT` | ❌ Violated | Constraint name lost |
| 51.18 | Predictable during dependency failures | First Stripe call hung for 30 s; later calls failed in 200 ms via the breaker | ❌ Violated | Inconsistent behaviour |

Sixteen of eighteen properties were violated. This is not a bad codebase — it is a **typical** one,
written in a hurry, with no correctness checklist.

## Fixing the top three by risk

Risk = severity (1–5) × likelihood (1–5).

| Property | Severity | Likelihood | Risk | Priority |
| -------- | -------- | ---------- | ---- | -------- |
| 51.9 No duplicate side effects | 5 | 3 | 15 | P0 |
| 51.8 Consistency preserved | 5 | 3 | 15 | P0 |
| 51.15 Cancellation not success | 4 | 3 | 12 | P1 |
| 51.10 Responses follow contracts | 3 | 4 | 12 | P1 |
| 51.1 Defined outcome | 4 | 2 | 8 | P2 |

### Fix 1 — 51.9: forward the idempotency key and make the dedupe atomic

```ts
// BEFORE
const charge = await stripe.charges.create({ amount, currency, source });
if (!(await redis.get(`idem:${key}`))) {
  await redis.set(`idem:${key}`, "1");
  await stripe.charges.create({ amount, currency, source });   // duplicated effect
}

// AFTER — the unique constraint arbitrates; Stripe's key dedupes at the provider.
export async function createAttempt(key: string, req: CheckoutRequest): Promise<Attempt> {
  const row = await db.query(
    `INSERT INTO checkout_attempts (tenant_id, idempotency_key, status, payload)
     VALUES ($1, $2, 'pending', $3)
     ON CONFLICT (tenant_id, idempotency_key) DO NOTHING
     RETURNING id, status`,
    [req.tenantId, key, JSON.stringify(req)],
  );
  if (row.length === 0) {
    const existing = await db.query(
      `SELECT id, status FROM checkout_attempts WHERE tenant_id=$1 AND idempotency_key=$2`,
      [req.tenantId, key],
    );
    return existing.rows[0];                 // replay the original attempt
  }
  return row.rows[0];
}

export async function chargeStripe(attempt: Attempt, amount: number) {
  return stripe.charges.create(
    { amount, currency: "usd", source: attempt.source },
    { idempotencyKey: `checkout:${attempt.id}` },   // 51.9 + provider-level dedupe
  );
}
```

### Fix 2 — 51.8 + 51.16: a step ledger with explicit states and guarded recovery

```sql
ALTER TABLE checkout_attempts
  ADD COLUMN state text NOT NULL DEFAULT 'pending',
  ADD COLUMN charge_id text,
  ADD COLUMN last_error_code text;

-- The state machine is now the schema. There is no way to be "charged but not active"
-- without the row saying so.
CREATE TYPE checkout_state AS ENUM
  ('pending','charging','charged','activating','active','failed','compensating','compensated','unknown');
```

```ts
export async function runCheckout(attempt: Attempt, ctx: OpContext): Promise<Outcome<Receipt>> {
  // 51.16: recovery decisions consult preconditions, and always give a reason.
  const decision = decideRecovery(ctx.lastError, { idempotent: true, deadline: ctx.deadline });
  if (decision.action === "stop") {
    await db.query(`UPDATE checkout_attempts SET state='failed', last_error_code=$2 WHERE id=$1`,
      [attempt.id, decision.reason]);
    return { status: "failed", error: appError(decision.reason) };
  }

  try {
    const charge = await chargeStripe(attempt, ctx.amount);   // 51.9
    await db.query(`UPDATE checkout_attempts SET state='charged', charge_id=$2 WHERE id=$1`,
      [attempt.id, charge.id]);                                // linearization point

    ctx.signal.throwIfAborted();                               // 51.15: cancellation check
    await activateSubscription(attempt);                       // 51.8
    await db.query(`UPDATE checkout_attempts SET state='active' WHERE id=$1`, [attempt.id]);

    return { status: "success", value: { attemptId: attempt.id, chargeId: charge.id } };
  } catch (err) {
    const appErr = toAppError(err, { operation: "checkout", attemptId: attempt.id });
    await db.query(
      `UPDATE checkout_attempts SET state=$2, last_error_code=$3 WHERE id=$1`,
      [attempt.id, stateFor(appErr), appErr.code]);            // 51.2: a record, always
    if (appErr.code === "PAYMENT_OUTCOME_UNKNOWN") {           // 51.16: ambiguous → resolve, don't retry
      await scheduleResolution(attempt.id);                    // read-back later
      return { status: "unknown", error: appErr, resolveBy: "next reconciliation run" };
    }
    throw appErr;                                              // 51.2: propagate to the boundary
  }
}
```

### Fix 3 — 51.15: cancellation is an outcome, not an exception swallowed by a catch

```ts
// The catch must distinguish cancellation from failure, or the operation continues
// after the client is gone and reports a success nobody receives.
catch (err) {
  if (ctx.signal.aborted) {
    const state = await readState(attempt.id);
    const outcome =
      state === "charged" || state === "active"
        ? { status: "success", value: { attemptId: attempt.id } }   // effect exists → truthful
        : { status: "cancelled" as const };                        // no effect → cancelled
    await recordOutcome(attempt.id, outcome);
    return outcome;
  }
  throw err;
}
```

## The remaining twelve violations, condensed

| Property | One-line fix |
| -------- | ------------ |
| 51.1 | Return `Outcome<Receipt>`; `null` is not an outcome |
| 51.2 | Every catch writes a terminal row or rethrows |
| 51.3 | One `classify()` at the Stripe adapter; handlers read the classification |
| 51.4 | `cause`, `stripeRequestId`, and `attempt` on the error object |
| 51.5 | Public DTO: code, message, correlation ID — no stack |
| 51.6 | Add a deadline (8 s) and a retry budget to `withRetry` |
| 51.7 | `await using conn = await pool.acquire()` |
| 51.10 | One `errorResponse()` builder + schema validation |
| 51.11 | Unknown → `500` + `UNCLASSIFIED` + alert; never `200` |
| 51.12 | `refreshToken()` retries at most once per operation |
| 51.13 | Unique constraint replaces the Redis check-then-act |
| 51.17 | Map SQLSTATE 23505 → `DB_UNIQUE_VIOLATION` and keep the constraint name |
| 51.18 | Give the Stripe client a breaker (20 requests / 50%) and a uniform degraded response |

## Key data / numbers

- **Properties violated in a typical pre-audit service: 12–16 of 18.** The audit is the point.
- **Risk scale**: severity 1–5 (1 = cosmetic, 5 = money/data loss) × likelihood 1–5 (1 = rare,
  5 = weekly). Risk 15+ = fix this sprint.
- **Audit time per flow**: ~3 hours for an 8-step flow with one engineer; the ledger and the
  oracle set are reusable for the next flow.
- **Violation discovery rate**: 60% of violations come from 3 properties (51.9, 51.8, 51.10).
  Audit those first.
- **Regression protection**: the injection matrix for Checkout has **7 failure points × 6 modes**
  = **42 cells**, of which 16 are now filled.
- **Post-audit outcome**: "duplicate charge" incidents 3/month → 0; "paid but no subscription"
  6/month → 0; contract violations 9/quarter → 0.

## Real-world use case — Acme SaaS `Checkout`, three months later

The audit above was performed on a real Acme checkout service. The three P0/P1 fixes shipped over
two sprints. Two observations from the rollout are worth more than the fixes themselves:

1. **The state machine in the schema was the highest-leverage change.** Making
   `checkout_attempts.state` an enum with a `charging`/`compensating` value meant that every
   "what happens if the pod dies here" question had an answer visible in a `SELECT`. Support
   tickets asking "did my payment go through?" dropped by half, because the support tool could
   read the row.
2. **The CI gate caught more than the audit.** Six weeks after the audit, a new developer added a
   `catch` that returned `null` in the refund path. The `no-empty-catch` and
   `no-null-return-in-catch` rules blocked the pull request. That violation would have cost a
   refund to be silently swallowed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Full property audit per flow | Complete, produces evidence | Days of work per flow | Critical flows (checkout, signup, provisioning) |
| Top-3 property audit | Fast, most value | Leaves quiet violations | Everything else |
| Automated property suite | Repeatable, scales | Needs injection seams and oracles | Once one flow is audited properly |
| External code review | Independent eyes | Expensive, varies in quality | Before a launch or a migration |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Record a verdict and evidence for every property | Mark a property "OK" because it looks fine |
| Rank violations by risk, not by ease of fixing | Fix the easiest violation first |
| Turn each finding into a regression test | File the audit and move on |
| Re-run the audit after a major refactor | Assume the audit survives the next architecture change |
| Audit the quiet properties explicitly (51.8, 51.9, 51.14, 51.15) | Only audit the loud ones |

## Checklist

- [ ] Every one of the 18 properties has a verdict for this flow.
- [ ] Every violation has a risk score, an owner, and a regression test.
- [ ] P0 violations (risk ≥ 15) are fixed before the next release.
- [ ] The findings that can be structural (types, policy tables, CI gates) were made structural.
- [ ] A reconciliation query exists to detect silent discards in this flow.
- [ ] The audit is scheduled to repeat after the next significant change.

## Related

- [Verifying Properties with Failure Injection](../02-deep-dive/01-verifying-properties-with-failure-injection.md)
- [Enforcing Properties Structurally](../02-deep-dive/02-enforcing-properties-structurally.md)
- [Chapter 52 — Failure-Path Analysis](../../52-failure-path-analysis/README.md)
- [Chapter 42 — Authentication, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
