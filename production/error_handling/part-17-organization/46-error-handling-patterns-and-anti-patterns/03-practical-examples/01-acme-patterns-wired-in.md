# Acme SaaS — All Twelve Patterns Wired Into One Path

> Part XVII · Chapter 46 · Sections 46.1–46.12 (applied) · _Estimated reading time: 18 min_
> **Prerequisite:** [Acme SaaS Error Module Tree](../../45-organizing-error-handling-modules/03-practical-examples/01-acme-error-module-tree.md)

## In one sentence

One request at Acme — `POST /checkouts/:id/capture` — plus its downstream saga and the async
export it can trigger, wired so that all twelve patterns (46.1–46.12, with 46.26 as the
baseline) appear at their correct layers, in the correct composition order.

## Why this matters in production

Patterns in isolation are textbook; patterns *composed* are architecture. The composition order
is where real systems go wrong: retries outside the boundary, fallbacks that serialize before
the handler, breakers that wrap the serializer. Seeing the full path end-to-end — every catch,
every policy reference, every serializing edge — is the fastest way to internalize where each
pattern is *allowed* to live.

## The path

```text
Client
  │ POST /checkouts/c_123/capture   (Idempotency-Key: k-9f2)
  ▼
transports/http/error-handler  ──── 46.1 global handler (last-resort exit)
  │ pre-handler: authz ──── 46.12 fail-safe (unknown permission → deny)
  ▼
checkout.service.capture ──── 46.26 simplest pattern baseline (typed throws)
  │ fail-fast guard: tenant suspended? → throw (46.11)
  │
  ├─ idempotency lookup (shared store) ──── replay prior success if key matched
  │
  ▼
shared/resilience: stripeBreaker ──── 46.7 (open → fast-fail, no Stripe call)
  │ closed state:
  ▼
withRetry("stripeHttp") ──── 46.6 named policy (3 attempts, full jitter, Retry-After)
  │
  ▼
infra/stripe adapter ──── 46.2/46.5 translation (Stripe shape → app errors, cause kept)
  │
  ▼
Stripe API ──── (vendor)
  │
  ├─ success ──▶ checkout-saga:
  │               step1 reserve inventory ──▶ step2 charge (above) ──▶ step3 activate
  │               failure at step3 → 46.10 compensation: refund(charge), release(hold)
  │
  ├─ CardDeclinedError ──▶ boundary decides: 402 via registry (no retry: not retryable)
  │
  └─ ExportJob scheduled (customer requested CSV with capture receipt)
        jobs/runner ──── 46.9 job boundary + withRetry("queueJob") + DLQ on exhaustion
        per-row parse ──── 46.3 Result<Row, ParseError> (collect-all semantics)
        optional AI note ──▶ boundary + 46.8 fallback (cached summary when LLM fails)
        registry ──▶ 46.4 single source for status/retryable/docs
```

## Worked example — the code at each numbered layer

```ts
// 46.12 authz middleware — unknown denies (fail-safe).
const decision = await authz.check(req.ctx, "checkout:capture", { checkoutId });
if (decision !== "allow") throw new PermissionError("AUTHZ_DENIED");

// 46.11 fail-fast guard at service entry — never reach Stripe with a suspended tenant.
const tenant = await tenants.get(req.ctx.tenantId);
if (tenant.status === "suspended") throw new TenantSuspendedError(tenant.id);

// 46.26 baseline: the service body is plain typed throws; no framework visible.
export async function capture(checkoutId: string, ctx: Ctx) {
  const checkout = await repo.find(checkoutId);
  if (!checkout) throw new CheckoutNotFoundError(checkoutId);          // → 404 via registry

  // 46.4 registry-backed idempotency: replay stored outcome for a matched key.
  const prior = await idempotency.find(ctx.idempotencyKey);
  if (prior) return prior.replay();                                    // same outcome, no charge

  // 46.7 + 46.6 + 46.2 composition: breaker outside, retry inside, translate innermost.
  const charge = await stripeBreaker.execute(() =>
    withRetry("stripeHttp", () =>
      stripe.charges.create(
        { amount: checkout.totalCents, currency: "usd" },
        { idempotencyKey: ctx.idempotencyKey },
      ).catch((err) => { throw fromStripeError(err); })));             // 46.2/46.5

  // 46.10 saga: later step fails → compensate the committed charge.
  try {
    await subscriptions.activate(checkout.tenantId, checkout.planId);
  } catch (err) {
    await payments.refund(charge);                                     // compensation
    sagaLog.record({ step: "activate", failed: true, refundOf: charge.id, cause: err });
    throw err;
  }

  await idempotency.store(ctx.idempotencyKey, checkout, charge);       // success replay data
  return charge;
}

// 46.3 ExportJob row loop — expected per-row failures are results, not throws.
for (const chunk of chunks) {
  const parsed = parseCsvChunk(chunk);
  if (!parsed.ok) { warnings.push(parsed.error); continue; }           // collect-all
  ingest(parsed.value);
}

// 46.8 optional feature boundary with an honest degraded value.
let aiNote: string | null = null;
try { aiNote = await agent.run(receiptContext); }
catch (err) { metrics.increment("ai_note.degraded"); /* fallback: null → UI placeholder */ }
```

The only catch that produces an external response is the 46.1 global handler
(`transports/http/error-handler.ts`), reading 46.4 registry metadata — nothing above it
serializes, nothing below it guesses a status.

## Key data

- **Composition order enforced at Acme:** `boundary → breaker → retry → adapter → vendor`.
  CI review checklist greps for `withRetry(` appearing *outside* a breaker when a breaker
  exists for that dependency, and for `fromStripeError` outside the adapter folder.
- **Attempt budget per capture:** ≤ 3 Stripe calls (policy), × 1 breaker fast-fail when open —
  worst case per logical op: 3, not the 12 of un-nested loops.
- **Pattern census on this one path:** all twelve patterns present; the number of *lines* they
  occupy outside 46.26's typed throws is small — resilience machinery ≈ 30 lines, everything
  else is ordinary business code. That ratio is the design's health metric.
- **DLQ contract:** exhausted `queueJob` retries publish the serializer's payload (code,
  category, attempt, correlationId) — replay tooling re-runs through the same boundary.

## Real-world use case — Acme SaaS

During the next Stripe incident (elevated 5xx for 40 minutes), this path degraded exactly as
designed: the breaker opened after 5 failures in 10 s, captures fast-failed with
`DEP_STRIPE_UNAVAILABLE` (503, retryable-by-client semantics), no compensation ran (no committed
charge), and Checkout's success-with-retry-from-mobile path — same idempotency key — landed
cleanly after the breaker half-opened at 30 s. Dashboard: Checkout conversion dipped ~4% for
the incident window and recovered; no double charges; DLQ empty (the job path never started).
Compare with the pre-pattern era of the same incident class (Chapter 45's god-module days):
multi-hour backlog, duplicate webhook processing, and ambiguous payment states. The patterns
did not make Stripe healthier; they made Acme's *response* boring — which is the entire goal.

## Trade-offs

| Aspect | This composition pays | This composition buys |
| ------ | --------------------- | --------------------- |
| Breaker + retry together | Two mechanisms to tune | Fast-fail when down; absorption when flaky |
| Idempotency storage | Extra writes per capture | Client/mobile retries become free |
| Saga + compensations | Refund failure modes to own | Cross-store consistency without 2PC |
| Result-typed row parsing | Verbose loop vs throw | Partial exports instead of total failures |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Compose in boundary → breaker → retry → adapter order | Put the boundary's serialization inside the service |
| Keep exactly one status decision (registry at the edge) | Compute HTTP status at multiple layers |
| Run compensations only for committed steps | Compensate a charge that never committed |
| Record idempotency success *after* the side effect commits | Store the key before the charge resolves |

## Common mistakes

- **Idempotency stored too early.** Recording the key before the charge resolves turns a
  timeout into a *replayed failure* — the retry finds a "success" entry that has no charge.
  Store on confirmed success; on ambiguity, store the AMBIGUOUS state for reconciliation.
- **Breaker opened by non-transient noise.** Counting `402 CardDeclined` as breaker failures
  opens the breaker on a sales spike of declined cards. Only transport-level/dependency
  classifications count as breaker failures.
- **Fallback around required steps.** The activate-subscription step has no fallback on
  purpose: a silently skipped activation is worse than a failed capture.

## Checklist

- [ ] Each pattern on the path lives in its zone file from Chapter 45's tree.
- [ ] One serializer, one status decision, one retry loop per operation.
- [ ] Idempotency replay covers mobile/client retries end-to-end.
- [ ] Compensation set matches the committed-step set exactly.
- [ ] Incident runbook cites the pattern numbers for each degradation mode.

## Related

- [Before/After Anti-Pattern Refactors](./02-before-after-anti-pattern-refactors.md)
- [Pattern Selection Trade-Offs](../02-deep-dive/01-pattern-selection-trade-offs.md)
- [The Error Lifecycle](../../../part-04-architecture/11-the-error-lifecycle/README.md)
