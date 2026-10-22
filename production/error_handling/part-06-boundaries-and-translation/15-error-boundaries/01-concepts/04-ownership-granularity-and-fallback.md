# Ownership, Granularity, and Fallback Behavior

> Part VI · Chapter 15 · Sections 15.13, 15.15, 15.17, 15.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Runtime Boundaries](./03-runtime-boundaries.md)

## In one sentence

Every boundary needs **one owner** who makes the final decision, a **granularity** small enough to
degrade locally but large enough to have a real fallback, and an explicit choice between
**isolating** (contain now) and **propagating** (let an outer owner decide).

## Why this matters in production

The two most common boundary bugs are **diffuse ownership** ("everyone catches, no one decides")
and **wrong granularity** (one global handler for all failures, or a `try/catch` around every
line). Both produce systems where failures are handled unpredictably. This file gives you the
decision rules.

---

## 15.13 — Ownership and responsibility

A boundary has exactly **one owner**: the layer that holds the context needed to make the outcome
decision. "Owner" is not the same as "who writes the `catch`." It is **who is accountable for the
terminal state** of the unit of work.

| Unit | Owner | Owns the decision to… |
| ---- | ----- | --------------------- |
| Request | Transport / controller | Set status, shape the response, redact |
| Transaction | Application service | Commit, roll back, compensate |
| Job | Worker / queue consumer | Retry, dead-letter, mark done |
| Process | Runtime bootstrap | Shut down cleanly or exit |
| Service contract | Service (API layer) | Map internal → protocol |
| Third-party call | Integration adapter | Translate, degrade, retry |
| UI subtree | Component / route | Show fallback, offer retry |

Two anti-patterns of ownership:

- **Shared ownership** — both the service and the controller catch and "decide," so the outcome
  depends on which fired first.
- **Orphaned ownership** — no layer is clearly accountable, so an error reaches the outermost
  handler that lacks the context to do anything meaningful.

```ts
// ❌ Diffuse ownership: repository + service + controller all "handle" the same error.
// repository
try { await db.insert(u); } catch (e) { log.warn(e); throw e; }        // logs, no decision
// service
try { await repo.create(u); } catch (e) { log.warn(e); throw e; }      // logs again, no decision
// controller
try { await svc.create(dto); } catch (e) { res.status(500).send(e.message); } // guesses
```

```ts
// ✅ Single ownership: repository translates; controller decides the transport outcome.
try {
  await repo.create(dto);             // throws DomainError | InfrastructureError
} catch (err) {
  return handleError(res, err);       // ONE decision point
}
```

**Invariant:** between the origin and the owner, `catch` blocks may **enrich** (add context) but
must not **decide** (swallow, substitute, or map to success).

## 15.15 — Correct granularity

Granularity is the scope of the boundary — how much code one `catch` protects. The right size is
**the smallest scope that owns a distinct fallback**.

| Granularity | Behavior on failure | Verdict |
| ----------- | ------------------- | ------- |
| **Too broad** — one global handler only | Whole request fails; no degradation | Under-isolated |
| **Too narrow** — `try/catch` per line | Noise, masking, unmaintainable | Over-instrumented |
| **Right-sized** — per feature/unit of work | Local degradation, clear owner | ✅ |

Decision rule:

```text
Is the fallback behaviorably different from just failing?  → boundary here
Is the fallback exactly "rethrow with context"?            → no boundary; enrich + propagate
Is the fallback undefined?                                 → no boundary; propagate to owner
```

Two heuristics to calibrate granularity:

1. **Feature granularity for optional work.** An optional enrichment (LLM summary, recommendation)
   gets its own boundary so its failure degrades one card, not the page.
2. **Tenant/job granularity for isolation.** One tenant's or one job's failure must not affect
   others — that is a bulkhead decision (Ch. 29) expressed as a boundary.

```ts
// Right-sized: one optional enrichment, one boundary, one fallback.
async function getDashboard(userId: string) {
  const [orders, billing] = await Promise.all([
    ordersRepo.recent(userId),
    billingRepo.summary(userId), // required — let failure propagate
  ]);

  let summary: string | null = null;
  try {
    summary = await llm.summarize(orders); // optional boundary
  } catch (err) {
    log.warn({ err }, "summary unavailable; degrading");
  }
  return { orders, billing, summary };
}
```

## 15.17 — Fallback behavior

A fallback is the substitute outcome used when the boundary decides not to propagate. It must be
**safe, explicit, and honest**.

| Fallback type | Example | Honesty requirement |
| ------------- | ------- | ------------------- |
| **Default value** | empty list, `null` summary | Mark it as absent, not "no data" |
| **Cached/stale** | last known exchange rate | Communicate staleness |
| **Deferred** | queue the work for later | Tell the user it is queued |
| **Reduced feature** | text-only instead of rich view | Do not silently change semantics |
| **Deny (fail-safe)** | block a risky action | Explain why (or be deliberately vague — Ch. 34) |

> ⚠️ **Hazard.** A fallback that returns a *plausible but wrong* value is worse than an error. A
> default of `0` for a failed balance read shows a wrong balance; `null` with "unavailable" is honest.

Rules:

- **Never silently convert failure to success.** A fallback is a *degraded* success with a signal,
  not a hidden failure (Ch. 2).
- **Fallbacks have their own failure mode.** If the cache fallback also fails, the boundary must
  escalate — not loop.
- **Log the degradation.** A fallback that fires constantly is a bug that hides as a feature.

```python
# Fallback with an explicit degradation signal (not a silent default).
def get_exchange_rate(pair: str) -> Rate:
    try:
        return provider.rate(pair)
    except TransientProviderError as e:
        cached = cache.get(pair)
        if cached is None:
            raise RateUnavailable(pair) from e   # no fallback available → escalate
        log.warning("using stale rate", extra={"pair": pair, "age_s": cached.age_s})
        return Rate(value=cached.value, stale=True, as_of=cached.as_of)
```

## 15.18 — Isolation vs propagation

This is the core boundary trade-off. **Isolation** contains the failure now; **propagation** passes
it to an owner who has more context.

| | Isolation (contain) | Propagation (let it travel) |
| --- | --- | --- |
| **When** | The unit can continue with a safe substitute | An outer layer owns the fallback/retry |
| **Effect** | Local degradation | Error reaches the correct owner |
| **Risk** | Hiding a real failure; masking | Surfacing a failure to a layer that can't act |
| **Example** | Empty recommendations list | Failed payment → request boundary returns `402` |

The choice is **per failure**, not global. A single request may isolate the LLM summary and
propagate the billing read failure.

```text
Failure: billing DB read times out
  Can the dashboard continue?         No — billing is required → PROPAGATE
  Does an outer layer have a fallback? The request boundary returns 503 + Retry-After
Failure: recommendations service 500s
  Can the page continue?              Yes → ISOLATE (empty list, log degradation)
```

Two guardrails:

1. **Isolate optional; propagate required.** The critical path should fail loudly; enrichments
   should fail quietly.
2. **Propagation is not abandonment.** When you propagate, attach context (`requestId`, domain
   label) so the owner can act — but do not swallow it on the way.

```go
// Optional dependency → isolate; required dependency → propagate with context.
recs, err := recommend(ctx, userID)     // optional
if err != nil {
    log.Warn("recommendations failed", "err", err)
    recs = nil                          // isolate
}
billing, err := billingSummary(ctx, userID) // required
if err != nil {
    return nil, fmt.Errorf("dashboard billing fetch: %w", err) // propagate, cause preserved
}
```

## Key data / numbers

- Node.js `unhandledRejection` terminates the process by default from Node 15+ — a process boundary
  must decide explicitly.
- React error boundaries do not catch event-handler, async, or data-fetch errors; those are
  separate isolation points.
- HTTP fallbacks should carry `Retry-After` (seconds or HTTP-date) when they are transient.

## Real-world use case — Acme SaaS

Acme's dashboard called four services. Originally one global handler meant any of them failing
500-ed the page. The team re-scoped: `billing` and `orders` are **required** (propagate; the request
boundary returns `503` with `Retry-After` when the DB is down), while `summary` (LLM) and
`recommendations` are **optional** (isolate; render placeholders and log a degradation). Blast
radius dropped from "whole dashboard" to "two cards," and on-call stopped paging for LLM timeouts.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each boundary exactly one owner | Let several layers each "handle" the same error |
| Right-size to the smallest distinct fallback | One global handler, or a catch per line |
| Isolate optional work; propagate required work | Treat the whole request as one fallback scope |
| Make fallbacks explicit and honest | Return plausible-but-wrong defaults |
| Attach context when propagating | Swallow on the way up |

## Common mistakes

- **Diffuse logging instead of a decision** — three layers log, none decides.
- **Fallback hides an outage** — a stale read silently served for days.
- **Optional dependency on the critical path** — an LLM timeout 500s the dashboard.
- **Propagating a required failure to a layer with no context** — a generic 500 instead of a
  precise `503`/`409`.

## Checklist

- [ ] Each boundary has one named owner accountable for the terminal state.
- [ ] Granularity is the smallest scope with a distinct fallback.
- [ ] Every fallback is explicit, honest, and logged.
- [ ] Optional work is isolated; required work propagates.
- [ ] Propagated errors carry context but are never swallowed.

## Related

- [Runtime Boundaries](./03-runtime-boundaries.md)
- [Nested Boundaries](../02-deep-dive/01-nested-boundaries.md)
- [Part XI — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
