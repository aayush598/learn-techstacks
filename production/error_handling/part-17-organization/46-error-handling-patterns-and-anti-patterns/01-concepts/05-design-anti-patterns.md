# Design Anti-Patterns: Five Ways Systems Decay

> Part XVII · Chapter 46 · Sections 46.17, 46.20, 46.23, 46.24, 46.25 · _Estimated reading time: 16 min_
> **Prerequisite:** [Handling Anti-Patterns](./04-handling-anti-patterns.md), [Shared Kernel vs App-Specific Code](../../45-organizing-error-handling-modules/01-concepts/02-shared-kernel-vs-app-specific.md)

## In one sentence

Five **design-level anti-patterns** — excessive custom error classes, repeated retry logic,
treating everything as retryable, retrying non-idempotent operations, and overengineering —
don't live in a single `catch` block; they live in the *shape* of the system, which is exactly
why they need architecture-scale refactors, not line edits.

## Why this matters in production

Code-level anti-patterns hide in functions; design anti-patterns hide in *conventions*. Nobody
writes "retry the charge twice" in one file — it emerges from three teams each adding their own
loop. Nobody designs 47 error classes on purpose — they accrete one "specific" subclass per
incident review. Because no single line looks wrong, these survive indefinitely while causing
the most expensive incidents in the catalog: double charges (46.24), retry storms (46.20/46.23),
and six-month infrastructure projects that ship nothing (46.25).

## 46.17 — Excessive custom classes

**What:** A proliferation of error subclasses that differ in *name* but not in *behavior* —
same category, same metadata, same handling — creating a nominal taxonomy nobody can navigate.

```ts
// ❌ 46.17 — 47 subclasses, all category "internal", all retryable false, all → 500.
class SaveUserError extends AppError {}
class SaveProjectError extends AppError {}
class SaveInvoiceError extends AppError {}
class LoadUserError extends AppError {}
// …44 more…
```

**Why it hurts:** `instanceof` ladders replace metadata reads; the type system carries no
routing information; every new engineer asks which of four "not found" classes to throw and
gets four different answers from four veterans. **Refactor:** collapse to *behavior classes*
(one type per distinct category/retryable/handling combination) and carry the specifics in
`code` + `details` fields (`ProjectNotFound` → `NotFound` with
`code: "PROJECT_NOT_FOUND"`). Expect a 5–10× reduction in class count.

## 46.20 — Repeated retry logic

**What:** Retry loops implemented independently at multiple call sites (or multiple layers for
the same call), each with its own constants and bug fixes.

**Why it hurts:** Divergent policies are indistinguishable in production until an incident
exposes them: service A honors `Retry-After`, service B ignores it; the worker's loop has
jitter, the API client's doesn't. Worse, *nested* repeats multiply attempts (3 × 5 = 15 calls
per logical operation under contention). **Refactor:** one retry implementation, named policies
in `shared/resilience/retry-policies.ts`, referenced by name; CI greps for numeric `attempts:`
outside that module. (This is the organizational face of 46.23.)

## 46.23 — Treating all failures as retryable

**What:** Retrying without consulting classification — retrying validation errors, `404`s,
declined cards, and signature failures the same as timeouts.

```ts
// ❌ 46.23 — five attempts against a permanent failure; user waits 30s for a certain 402.
for (let i = 0; i < 5; i++) {
  try { return await charge(card); }
  catch { await sleep(1000 * i); }
}
```

**Why it hurts:** Permanent failures are deterministic: attempt 2 will fail exactly like
attempt 1. The user eats the cumulative delay, the provider eats quota (a card-declined retry
burst can trip fraud controls), and the logs fill with identical failures that alert nobody.
During provider incidents, retry-all converts *their* partial outage into *your* full-load
amplification. **Refactor:** `retryOn: (e) => e.retryable` driven by adapter translation +
registry; unknown → non-retryable (fail-safe).

## 46.24 — Retrying non-idempotent operations

**What:** Re-executing an operation with side effects that are **not safe to repeat** — payment
captures, "create subscription", "send invitation email", non-keyed writes — after an ambiguous
failure (timeout, connection reset mid-response).

**Why it hurts:** This is the anti-pattern that costs money directly: the first attempt
succeeded server-side, the client saw a timeout, attempt two captures again → **double charge**.
It is the highest-severity item in this entire chapter, and it is frequently invisible until a
customer or an auditor finds it. **Refactor, in order:**

1. Make the operation idempotent (idempotency keys on payments; deterministic ids on creates).
2. If true idempotency is impossible, do **not** auto-retry: surface the ambiguous outcome
   (typed `AMBIGUOUS_OUTCOME`) and reconcile asynchronously (Chapter 23's uncertain-persistence
   rules).
3. Encode the decision in the policy: `retryOn` must be false for non-idempotent ops without
   keys — enforced in the shared retry module, not by convention.

```ts
// ✅ capture with an idempotency key; retry is then safe by construction.
await withRetry("stripeHttp", () =>
  stripe.charges.create({ amount, currency }, { idempotencyKey: checkoutId }));
```

## 46.25 — Overengineering

**What:** Building generality the system does not need: a saga orchestrator for a two-step
flow, a circuit breaker for a single internal call with no outage history, a universal
error-pipeline framework with middleware hooks, result types everywhere including the CLI
throwaway script.

**Why it hurts:** Opportunity cost and *risk*: every abstraction is a place for wrong
assumptions to hide; a framework's bugs are harder to see than a missing try/catch; and the
team ships infrastructure instead of product for a quarter. It is an anti-pattern *of good
intentions*, which is why it needs an explicit rule rather than taste. **Refactor / prevent:**

- The simplest pattern (46.26) is the default; each mechanism (retry, breaker, fallback,
  compensation, result) requires a *measured* justification: which incident, which number?
- Rule of three: build the abstraction on the third concrete use, not the first.
- Kill criteria: if the abstraction has one consumer after two quarters, delete it.

## Key data

- **Class-count sanity:** behavior-distinct error types for a mid-size SaaS: ~15–30, not 100+.
  Acme's collapse: 61 subclasses → 14 behavior types + 45 codes, with zero routing changes
  (routing already read metadata).
- **Retry-divergence signature:** ≥ 2 numeric `attempts` constants for the same dependency
  class = a live 46.20. Acme's pre-refactor count: 7 constants for 3 dependencies.
- **Non-idempotent retry exposure:** every write path with a retry loop and no idempotency key
  is a billing-incident candidate; audit count at Acme was 3 (all fixed with keys or
  AMBIGUOUS_OUTCOME surfacing).
- **Overengineering budget check:** mechanisms without a named incident/number justification:
  typically 2–4 per team at audit time; each is a deletion candidate.

## Real-world use case — Acme SaaS

The Checkout incident review after a double-charge escalation: attempt 1 of
`POST /checkouts/:id/capture` timed out client-side at 10 s *after* Stripe committed the
capture. The mobile client's inline retry (46.20, constants: 3 attempts, no jitter) re-sent;
the server had no idempotency key on the capture (46.24); and the error classifier marked all
Stripe 5xx *and* timeouts as retryable without distinguishing ambiguous outcomes (46.23's
cousin). One customer was charged twice; the refund took nine days. Remediation in the order
from 46.24: capture gained `idempotencyKey: checkoutId`, the shared policy's `retryOn` excluded
non-keyed captures, and ambiguous outcomes were typed `PAYMENT_AMBIGUOUS_OUTCOME` and routed to
a reconciliation queue instead of a client retry. Repeat occurrences since: zero. The mobile
inline retry loop was deleted — client retries re-sent the *same* idempotent request, which
collapsed 46.20 as well.

## Trade-offs

| "Fix" | Buys | Pays | Verdict |
| ----- | ---- | ---- | ------- |
| One error class per code (more classes) | Readable names | Nominal taxonomy; instanceof lattices | Wrong direction if behavior is identical |
| Behavior classes + codes (46.17 fix) | Metadata-driven routing | Requires registry discipline | Right |
| Shared retry module (46.20/23 fix) | Consistency; auditability | One shared thing to version | Right past 2 call sites |
| No retries at all (reaction to 46.23/24) | Safety | Users eat transients | Too blunt; classify instead |
| Minimal mechanisms per need (46.25 fix) | Speed; fewer bugs | Rebuild a bit later if need grows | Right default |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Create a new class only for distinct *behavior* | Subclass per entity or per endpoint |
| Require a named policy reference for every retry | Let teams "just loop it" locally |
| Gate `retryOn` on classification + idempotency | Retry on catch, unconditionally |
| Demand a measured justification per mechanism | Ship breakers/sagas/frameworks speculatively |

## Common mistakes

- **Collapsing classes but keeping instanceof switches.** The refactor is incomplete: convert
  switches to metadata reads, or the taxonomy just moved from types to strings.
- **Adding keys without key-storage semantics.** An idempotency key must be stored with the
  response for replay (Chapter 28); a key that isn't persisted protects nothing.
- **Deleting "unused" fallbacks that were load-bearing in an untested incident path.** Apply
  the kill criterion only after exercising the incident runbook that would have used them.
- **Treating 46.25 as "never build."** At scale, shared retry and registry infrastructure are
  the *measured* answer; the anti-pattern is building them without evidence, not building them.

## Checklist

- [ ] Error subclass count ≈ behavior-distinct handling, not entity count.
- [ ] Zero numeric retry constants outside the shared policy module.
- [ ] Zero retry loops whose predicate ignores `e.retryable`.
- [ ] Every retried write path is keyed or explicitly classified non-retryable.
- [ ] Each resilience mechanism has a written justification (incident or number).

## Related

- [Handling Anti-Patterns](./04-handling-anti-patterns.md)
- [Pattern Selection Trade-Offs](../02-deep-dive/01-pattern-selection-trade-offs.md)
- [Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
