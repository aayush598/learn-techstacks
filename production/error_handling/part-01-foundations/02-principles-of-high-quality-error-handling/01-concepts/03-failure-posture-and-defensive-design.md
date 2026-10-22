# Failure Posture and Defensive Design

> Part I · Chapter 2 · Sections 2.7, 2.8, 2.9, 2.10, 2.11 · _Estimated reading time: 24 min_

## In one sentence

Every fallible operation must declare a **posture** — fail-fast, fail-safe, or degrade gracefully —
and your defensive code must be **proportionate** to real threats while never surprising the reader.

## Why this matters in production

Posture is the single most consequential choice in error handling, and the one most often made by
accident. A payment path that "degrades" by charging nothing loses revenue. A read-only dashboard
that fails fast because a *non-critical* ad service is down is needless downtime. Getting posture
wrong is how you turn a 1% dependency hiccup into a 100% outage — or a silent financial loss.

## Core concept — five principles

### 2.7 Fail-fast design

**Stop immediately when continuing would be unsafe or would hide a defect.** Fail-fast is correct
for programming errors, invariant violations, and corrupt input.

```ts
// ✅ Fail-fast on an impossible state — do not limp along.
if (!config.stripeSecretKey) {
  throw new ConfigurationError("STRIPE_SECRET_KEY is required at startup");
}
```

Fail-fast is the default for **deterministic** and **unrecoverable** failures (Chapter 1).

### 2.8 Fail-safe design

**On failure, stay in a safe state** — often by denying or blocking — even at the cost of
availability. This is the default posture for **security** and **integrity** decisions.

| Decision | Safe-on-failure behavior |
| -------- | ------------------------ |
| Authorization check | Deny (fail-closed) |
| Signature verification | Reject the webhook |
| Funds availability | Do not pay out |
| Config parsing | Refuse to start |

> ⚠️ **Hazard.** Fail-open (allow on failure) is sometimes chosen for availability. That is a
> deliberate, documented risk decision (Chapter 30), never a default.

### 2.9 Graceful degradation

**Keep serving a reduced feature set** when a *non-critical* dependency fails. Degradation is
correct only when the feature is optional and the fallback is honest.

```ts
// ✅ Non-critical: recommend() is optional; degrade to an empty list.
let items: Item[] = [];
try {
  items = await recommend(userId);
} catch (err) {
  log.warn({ err, userId }, "recommendations degraded");
}
// page still renders; no false data presented
```

Degradation must never fabricate data that looks real (Chapter 30).

### 2.10 Defensive vs excessive defensive programming

| Defensive (✅) | Excessive (❌) |
| -------------- | -------------- |
| Validate at trust boundaries | Re-validate internally-typed values everywhere |
| Handle the failures you can name | `try/catch` around every line "just in case" |
| Assert invariants | Silently coerce invalid state |
| Fail-safe on security decisions | Fail-safe that hides bugs |

Excessive defense **masks faults** — the exact thing Chapter 1 warns against. Defense belongs where
untrusted input, external systems, or genuine uncertainty exist.

### 2.11 Principle of least surprise

Failure behavior should match what a reasonable engineer expects from the name and signature.

- A function named `getUser` that *creates* a user surprises everyone.
- A `save()` that returns success while dropping data surprises everyone.
- A `validate()` that throws on the first field but returns a list for others surprises.

Least surprise means consistent verbs, honest names, and predictable failure semantics.

## How it works (mechanics) — choosing a posture

```text
                   Is the failure recoverable?
                   ┌───────────no──────────┐
                   │                       │
             is it deterministic?     is it recoverable?
                   │                       │
              yes  │  no              yes  │  no
                   ▼   ▼                  ▼   ▼
              FAIL-FAST   (ambiguous)  RETRY / DEGRADE   FAIL-SAFE
              (bug)        isolate →   (transient,        (integrity,
                           timeout)     optional dep)      security)
```

Decision rules:

1. **Programming/invariant error** → fail-fast, fix the fault.
2. **Transient, idempotent, recoverable** → retry (Chapter 27).
3. **Optional dependency down** → degrade (Chapter 30).
4. **Security/integrity decision** → fail-safe (deny).
5. **Critical dependency down** → fail-fast at request level, return `503`.

## Worked example

**Checkout** in Acme SaaS touches two dependencies: the payment gateway (critical) and a
fraud-scoring service (high value but configurable).

```python
# Posture per dependency, made explicit.
def checkout(cart) -> Result[Order, CheckoutError]:
    # Critical → fail-fast if unavailable.
    if not payments.healthy():
        return Err(PaymentProviderUnavailable())      # → 503, retryable

    # Non-critical → degrade honestly: skip scoring, flag for review.
    try:
        score = fraud.score(cart)
    except FraudServiceError:
        score = None                                  # degraded, not fabricated
        flag_for_manual_review(cart)

    if score is not None and score > RISK_THRESHOLD:
        return Err(OrderFlaggedForReview())           # fail-safe on risk
    return Ok(payments.capture(cart))                 # captures only once (idempotent)
```

Each line chooses a posture deliberately: **fail-fast** (critical dep), **degrade** (scoring),
**fail-safe** (risk), **retry** (handled by the payments client).

## Key data / numbers

| Item | Value | Why |
| ---- | ----- | --- |
| Dependency unavailable | `503 Service Unavailable` + `Retry-After` | Critical dep fail-fast |
| Gateway timeout | `504 Gateway Timeout` | Upstream late |
| Degraded response | `200` with `X-Degraded: true` (custom) | Honest partial result |
| Signature tolerance | Stripe default 300s | Fail-safe on stale webhook |
| Circuit breaker open | fail-fast/half-open after threshold (e.g. 5 failures) | Prevents fan-out |
| Authz on check failure | deny (fail-closed) | Integrity default |

## Real-world use case — Acme SaaS

Acme's project dashboard embedded an LLM summary and a live activity feed. Initially both failures
propagated: an LLM outage 500-ed the whole dashboard. Applying posture principles, the team marked
**LLM summary as optional** (degrade to cached or "unavailable") and **activity feed as critical**
serving from the primary store. Dashboard availability rose from 99.2% to 99.95% because a
non-critical feature could no longer take down a critical one. The LLM stayed on the page as a
*feature*, not a *dependency*.

## Trade-offs

| Posture | Pros | Cons | When to use |
| ------- | ---- | ---- | ----------- |
| Fail-fast | Surfaces defects, no corrupt state | Can turn blips into errors | Bugs, invariants, critical deps |
| Fail-safe | Protects data/security | Reduced availability | Auth, payments, integrity |
| Degrade | Keeps product usable | Risk of serving stale/partial | Optional deps, read paths |
| Fail-open | Maximum availability | Risk security/data | Explicit, rare, documented |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Choose and document a posture per dependency | Decide posture by accident |
| Degrade only on honest fallbacks | Serve fabricated data as real |
| Fail-safe on security decisions | Fail-open by default |
| Defend at trust boundaries | Wrap every line defensively |

## Common mistakes

- **Fail-fast on a non-critical dep** → avoidable outages.
- **Degrade into silent inaccuracy** → users trust wrong data.
- **Fail-open security** → authz bypass when the checker errors.
- **Defensive noise** → catch blocks everywhere that hide the real defect.

## Checklist

- [ ] Does each fallible operation have a named posture?
- [ ] Are optional dependencies isolated with a fallback?
- [ ] Are security/integrity decisions fail-safe?
- [ ] Is defensive code proportional to real, named risks?
- [ ] Would a new reader be surprised by any failure behavior?

## Related

- [Fail-Fast, Fail-Safe, and Degradation — Deep Dive](../02-deep-dive/01-fail-fast-fail-safe-and-degradation.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 1 — Classification Dimensions](../../01-understanding-errors-and-failures/01-concepts/02-the-fifteen-dimensions.md)
- [Glossary: fail-fast, fail-safe, graceful degradation](../../../GLOSSARY.md)
