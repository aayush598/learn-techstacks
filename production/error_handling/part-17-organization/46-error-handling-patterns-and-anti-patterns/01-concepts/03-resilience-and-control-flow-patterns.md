# Resilience and Control-Flow Patterns — Including the Simplest Pattern

> Part XVII · Chapter 46 · Sections 46.6, 46.7, 46.8, 46.11, 46.12, 46.26 · _Estimated reading time: 17 min_
> **Prerequisite:** [Modeling Patterns](./02-modeling-patterns.md), [Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)

## In one sentence

Six patterns govern *what happens next* after an error is typed: **retry policy**, **circuit
breaker**, and **fallback** manage dependency failures, **fail-fast** and **fail-safe** choose
the direction of abort, and the **simplest pattern** — a typed error thrown and caught at the
boundary — is the legitimate default that all the others must earn their way past.

## Why this matters in production

These six decide whether a provider blip becomes a five-minute wobble or a SEV-1. Retry without
a policy amplifies outages; a fallback without a boundary hides them; fail-open on an authz check
converts an availability choice into a security incident. And the inverse failure is equally
real: teams under-invest in the default and over-invest in machinery — six months of building a
resilience framework for a CRUD app (46.25). Knowing the default is *good* is what keeps the
catalog honest.

## Pattern 46.6 — Retry policy

**What:** Re-execute a failed operation **iff** it is classified retryable, using a *named,
shared* policy: bounded attempts, exponential backoff, full jitter, honoring server-provided
`Retry-After`, and (at scale) a retry budget.

**Solves:** Transient failures (timeouts, `429`, `57014`, connection resets) are absorbed
without user impact. The *named policy* is the organization fix: numbers live in one module,
not at call sites.

**Must not:** Retry non-retryable classifications (validation, `404`, declined cards), retry
non-idempotent operations without an idempotency key, or nest retry loops across layers.

```ts
// shared/resilience/retry.ts — one implementation, referenced by name.
export async function withRetry<T>(policyName: RetryPolicyName, fn: () => Promise<T>) {
  const p = RETRY_POLICIES[policyName];
  for (let attempt = 1; ; attempt++) {
    try { return await fn(); }
    catch (err) {
      const e = toAppError(err);
      if (!p.retryOn(e) || attempt >= p.attempts) throw e;      // preserve final failure
      await sleep(jitter(p.baseDelayMs * p.multiplier ** (attempt - 1), e));
    }
  }
}
```

## Pattern 46.7 — Circuit breaker

**What:** A state machine around a dependency — **closed** (normal), **open** (failing fast
without calling), **half-open** (trial calls) — that opens after a threshold of failures and
closes again after trial successes.

**Solves:** Cascading failure and resource exhaustion: when Stripe is down, callers stop
*calling* Stripe, freeing threads/connection-pool slots for work that can succeed. Failures
fail fast with a typed `DependencyOpen` error instead of piling up in timeouts.

**Must not:** Replace retries (they compose: retry inside breaker's closed state), sit around
non-remote code, or share one breaker across unrelated dependencies.

```ts
// shared/resilience/breakers.ts — one breaker per critical dependency class.
export const stripeBreaker = new CircuitBreaker({
  failureThreshold: 5,       // within rolling window:
  windowMs: 10_000,          //   → open
  openMs: 30_000,            //   → then half-open
  halfOpenMaxCalls: 2,       //   trial calls; all succeed → closed
});
// usage: await stripeBreaker.execute(() => withRetry("stripeHttp", () => charge(...)));
```

## Pattern 46.8 — Fallback

**What:** When the primary path fails (often after breaker-open), serve a defined substitute:
cached data, a secondary provider, a degraded feature set, a queued-for-later outcome.

**Solves:** Optional features stay useful during dependency incidents (cached summary instead
of no summary). Required features get *defined* degraded modes (read-only, feature-flagged
off) instead of undefined outages.

**Must not:** Silently substitute inaccurate data for accurate data (a stale billing total is
not a fallback, it is a bug), cascade through multiple fallback layers without bounds, or apply
to writes that cannot be safely substituted.

## Pattern 46.11 — Fail-fast

**What:** Abort the current operation immediately upon detecting an invalid precondition,
rather than continuing with bad state.

**Solves:** The compounding-damage class of bugs: a missing tenant config detected at service
entry cannot reach the payment step. Validation at the trust boundary is fail-fast; `assert`
on internal invariants is fail-fast; refusing to start with broken config is fail-fast.

**Must not:** Be confused with failing *loudly to the user* — fail-fast internally still maps
to a clean 4xx at the boundary. And it must not be applied where partial progress is the
desired semantic (batch imports need collect-all, not fail-fast).

## Pattern 46.12 — Fail-safe

**What:** When a component cannot determine the safe outcome, choose the state that preserves
safety — typically **deny** (authorization), **do not commit** (transactions), **do not retry**
(unknown classification) — even at the cost of availability.

**Solves:** The security/consistency default. Unknown permission result → deny. Unknown
whether a charge committed → do not auto-retry without idempotency key; surface as ambiguous.
Unknown vendor error → non-retryable, page a human.

**Must not:** Be applied where the product has explicitly chosen fail-open (e.g. a
non-critical recommendation widget degrading open is a product decision, documented as such).

```ts
// Fail-fast + fail-safe at the authz edge — deny is the safe outcome.
export async function authorize(req: AuthzRequest): Promise<void> {
  const result = await policy.check(req);          // may throw (infra) or return unknown
  if (result === "deny" || result === "unknown") { // unknown → deny (fail-safe)
    throw new PermissionError("AUTHZ_DENIED");
  }
}
```

## Pattern 46.26 — The simplest pattern

**What:** A typed error (extending the kernel base, carrying a registry-backed code) is
**thrown in the layer that detects it and caught once at the boundary** that owns the fallback
— with no result types, no retry framework, no breaker, no saga. For many operations this is
not a shortcut; it is the complete, production-grade answer.

**Solves:** Overengineering (46.25). It is the baseline every more complex pattern must justify
beating: "what does the breaker buy us that throw-and-catch-at-boundary doesn't?" If the answer
isn't concrete (measured timeout waste, cascade risk), keep the simple version.

**Must not:** Become an excuse for missing boundaries (there must still be exactly one defined
exit) or for missing classification (the error still needs a code and registry entry).

```ts
// 46.26 in full: this IS production-grade. Three files: error, call site, handler.
export class ProjectNotFoundError extends AppError {
  readonly code = "PROJECT_NOT_FOUND";
  readonly category = "not_found" as const;
}
const project = await repo.find(id);
if (!project) throw new ProjectNotFoundError();
// transports/http/error-handler.ts maps PROJECT_NOT_FOUND → 404 via the registry. Done.
```

## Key data

- **Retry defaults:** attempts 3 (sync) / 5 (jobs); full jitter; multiplier 2–4;
  `Retry-After` overrides computed delay; budgets cap retries to a small fraction of primary
  traffic (a common starting cap: retries ≤ 10% of requests per dependency per hour).
- **Breaker defaults worth copying:** 5 failures / 10 s window → open; 30 s open → half-open;
  2 consecutive half-open successes → closed. Tune from observed incident data, not aesthetics.
- **Fail-safe defaults:** unknown authz → deny; unknown classification → non-retryable;
  ambiguous commit → no automatic retry without idempotency key; unparseable webhook signature
  → reject (400), never process.
- **When the simple pattern suffices (rule of thumb):** operations with low call volume, no
  cascade risk, and expected failure < ~1% need only 46.26 + the global handler.

## Real-world use case — Acme SaaS

`AgentRun` launched with the full stack up front: a retry wrapper, a breaker on the LLM
provider, and a fallback chain (primary model → smaller model → cached template). Six weeks in,
the team measured: the breaker never opened (provider SLA was high), the fallback chain fired
twice, and the retry wrapper's nested `withRetry` inside the provider SDK produced double
retries on rate limits. Meanwhile `ExportJob` — still on the simple pattern (typed errors,
`runJob` boundary, DLQ) — had *better* incident metrics because its failures were classified
correctly. The corrective action was subtractive for AgentRun: keep adapter translation +
named retry policy (46.6), drop the unused breaker and one fallback layer (defer until
measured need). Framework lines of code: −60%; no user-visible regression.

## Trade-offs

| Pattern | Buys | Costs | Earn it when |
| ------- | ---- | ----- | ------------ |
| Retry policy | Absorbs transients invisibly | Amplification risk; needs classification | Failures are transient AND operation is idempotent (or keyed) |
| Circuit breaker | Stops cascade; frees resources | State to operate/tune; false opens | Dependency has real outage modes and shared resources at risk |
| Fallback | Keeps optional features alive | Freshness/accuracy trade-offs; complexity | Feature is optional AND a defined degraded mode exists |
| Fail-fast | Stops compounding damage | Requires precondition knowledge | Invalid state would cause worse downstream failure |
| Fail-safe | Safety under uncertainty | Availability cost | Decision affects security, money, or data integrity |
| Simplest pattern (46.26) | Minimal code; easy to reason | No absorption of transients; blast radius = boundary's | Default. Everything else must beat it. |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reference retry policies by name | Inline attempt counts at call sites |
| Compose breaker outside retry, per dependency | Wrap everything in one global breaker |
| Default unknown → non-retryable, unknown authz → deny | Default-allow or default-retry on unknown |
| Require measured justification to exceed 46.26 | Start every feature with the full resilience stack |

## Common mistakes

- **Retry inside the adapter *and* the caller** — nested loops multiply attempts (classic
  amplification). Adapters translate only; one layer owns the loop.
- **Breaker without timeouts.** A breaker counts failures; without per-call timeouts, "failures"
  are hangs, and the breaker never trips. Timeouts first (Chapter 29).
- **Fallback that hides writes.** Falling back to "queue it and return success" for a payment
  changes the contract from synchronous failure to eventual surprise. Writes fail explicitly.
- **Treating 46.26 as a strawman.** It is not: many teams ship it as their target state for
  entire bounded contexts, correctly.

## Checklist

- [ ] Every retry references a named policy; no numeric attempts outside it.
- [ ] Breakers exist per critical dependency, with timeouts underneath.
- [ ] Every fallback has a defined, documented degraded value (and a comms plan).
- [ ] Unknown classification defaults to non-retryable; unknown authz defaults to deny.
- [ ] Each feature can answer: "why aren't we on the simplest pattern yet?"

## Related

- [Anti-Pattern Design Failures](./05-design-anti-patterns.md)
- [Pattern Selection Trade-Offs](../02-deep-dive/01-pattern-selection-trade-offs.md)
- [Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
