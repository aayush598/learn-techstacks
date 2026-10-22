# Refactoring Toward the Principles — Before / After

> Part I · Chapter 2 · All sections · _Estimated reading time: 26 min_

## In one sentence

The principles only matter if they change real code, so this file takes five realistic
before/after refactors — drawn from the recurring cast — and labels **which principle** each change
applies.

## Why this matters in production

Abstract principles are easy to nod at and hard to apply under deadline. Seeing the *diff* — the
exact lines that change — is what lets you spot the same shape in your own codebase and fix it
without a rewrite.

## Worked example 1 — Checkout: failure → success (2.15) + preserve cause (2.13)

```python
# ❌ BEFORE: a failed charge is reported as a successful, empty result.
def charge(order):
    try:
        resp = gateway.charge(order.amount, idempotency_key=order.id)
    except requests.RequestException:
        return {"status": "ok", "charge_id": None}   # 2.15 failure→success
    return {"status": "ok", "charge_id": resp.id}
```

```python
# ✅ AFTER: outcome is explicit; the cause is preserved; no fake success.
def charge(order) -> Result[Charge, PaymentError]:
    try:
        resp = gateway.charge(order.amount, idempotency_key=order.id)
    except gateway.RateLimited as e:
        raise TransientError("gateway rate limited") from e   # 2.13 preserve cause
    except gateway.Declined as e:
        return Err(PaymentDeclined(reason=e.reason))          # 2.7 permanent, non-retryable
    return Ok(Charge(id=resp.id, amount=order.amount))
```

**Principles applied:** 2.15 (no fake success), 2.13 (cause), 2.1 (explicit outcome), 2.18
(predictable: declined is never retried).

## Worked example 2 — WebhookIngest: swallow (2.14) + predict (2.18)

| Before | After | Principle |
| ------ | ----- | --------- |
| `except Exception: pass` | classify: signature / duplicate / transient | 2.14, 2.18 |
| always `200` | `400` bad signature, `200` duplicate, `500` retryable | 2.2, 2.18 |
| no event id recorded | idempotency on `event.id` | 2.3 (first-class outcome) |

```ts
// ✅ AFTER — the catch does something observable and the status is predictable.
try {
  await processEvent(event, { idempotencyKey: event.id });
  res.status(200).json({ ok: true });
} catch (err) {
  if (err instanceof SignatureError) return res.status(400).json({ code: "WEBHOOK_SIGNATURE_INVALID" });
  log.error({ err, eventId: event.id }, "ingest failed");
  res.status(500).json({ code: "WEBHOOK_PROCESSING_FAILED" });
}
```

## Worked example 3 — ExportJob: separation (2.4) + central policy (2.5)

```go
// ❌ BEFORE: the worker decides retry, status, and logging inline; policy drifts per job.
func handle(msg Message) error {
    if err := export(msg); err != nil {
        if strings.Contains(err.Error(), "timeout") {   // stringly-typed policy
            return retrySameJob(msg)                     // unbounded, no backoff
        }
        return nil                                       // 2.14 swallowed
    }
    return nil
}
```

```go
// ✅ AFTER: worker calls one policy; retry/classification is centralized.
func handle(ctx context.Context, msg Message) error {
    // job.Run applies the shared policy: classify, backoff, max attempts, DLQ.
    return job.Run(ctx, msg, job.Policy{
        MaxAttempts: 5,
        Backoff:     job.ExponentialJitter,
        Retryable:   job.RetryableCodes{SQLState40001, HTTP429, HTTP503},
    }, export)
}
```

**Principles applied:** 2.4 (domain does work; policy separate), 2.5 (one policy), 2.19
(boilerplate removed via `job.Run`), 2.6 (single responsibility).

## Worked example 4 — Acme API: inconsistent mappings (2.2) → one registry

```text
  BEFORE (drift)                        AFTER (registry)
  ─────────────────────────────         ─────────────────────────────
  POST /users  duplicate → 200          every duplicate           → 409
  POST /teams  duplicate → 409          every validation failure  → 422
  POST /invites duplicate → 500         every not-found           → 404
  validation on /users → 400            every upstream timeout    → 504
  validation on /teams → 422
```

```yaml
# ✅ AFTER: one policy table drives every route.
mappings:
  VALIDATION_FAILED:      { http: 422, retryable: false }
  DUPLICATE_RESOURCE:     { http: 409, retryable: false }
  RESOURCE_NOT_FOUND:     { http: 404, retryable: false }
  UPSTREAM_TIMEOUT:       { http: 504, retryable: true }
```

**Principles applied:** 2.2 (consistency), 2.5 (central policy), 2.18 (predictable).

## Worked example 5 — AgentRun: redundant handling (2.16) + catch-and-rethrow (2.17)

```ts
// ❌ BEFORE: three layers retry and log the same provider error.
// repo:
try { return await provider.complete(p); } catch (e) { log.warn(e); throw e; }
// service:
try { return await repo.complete(p); } catch (e) { log.warn(e); throw e; }   // retry #2
// controller:
try { return await service.complete(p); } catch (e) { log.error(e); throw new AgentError("failed"); }
```

```ts
// ✅ AFTER: one owner (the adapter) retries; others propagate; the top translates once.
// adapter:
export async function complete(p: Prompt) {
  return withRetry(() => provider.complete(p), { attempts: 4, backoff: "exp-jitter" });
}
// service: no catch — propagate.
// controller:
catch (err) { throw toAppError(err); }  // translate once, preserve cause
```

**Principles applied:** 2.16 (single handling layer), 2.17 (no bare rethrow), 2.13 (cause),
2.6 (single responsibility).

## Key data / numbers

| Item | Value | Principle served |
| ---- | ----- | ---------------- |
| Duplicate create | `409` | Consistency (2.2) |
| Validation | `422` | Consistency (2.2) |
| Upstream timeout | `504`, retryable | Predictability (2.18) |
| Default retry budget | 3–5 attempts, exp backoff + jitter | Central policy (2.5) |
| Stripe idempotency retention | 24h | Explicit contract (2.1) |
| PostgreSQL `40001` | serialization_failure → retry | Preserved cause (2.13) |

## Real-world use case — Acme SaaS

Acme performed all five refactors over one quarter, in risk order: first the payment fake-success
(2.15, highest risk), then webhook swallowing (2.14), then export policy centralization (2.5), then
the API mapping registry (2.2), then AgentRun de-duplication (2.16). No single change was large;
together they cut error-related incidents by roughly two-thirds and dropped mean time to diagnose
from hours to under twenty minutes, because every failure now had a stable, classified, cause-
preserving signal.

## Trade-offs

| Refactor | Risk | Payoff | Do first when |
| -------- | ---- | ------ | ------------- |
| Remove failure→success | High if rushed | Very high | Money/data involved |
| Preserve cause | Low | High | Always |
| Centralize policy | Medium | High | Mapping drift exists |
| Remove redundant handling | Low | Medium | Double-retry/double-log observed |
| Consistent mappings | Medium (breaking) | High | Public API clients exist |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Refactor in risk order, one principle at a time | Rewrite all handling at once |
| Add a regression test per refactor | Trust that behavior is unchanged |
| Version-map before changing public statuses | Flip statuses with no deprecation |
| Keep the diff reviewable | Bundle unrelated principle fixes |

## Common mistakes

- **Big-bang rewrite** of error handling — untestable and destabilizing.
- **Changing public status codes** without a deprecation window (Chapter 49).
- **Removing a catch** without confirming an outer boundary exists.
- **Deduplicating retries** but forgetting to preserve the final failure.

## Checklist

- [ ] Did each change map to a named principle?
- [ ] Is there a test that fails before and passes after?
- [ ] Were public contract changes versioned?
- [ ] Is the outer boundary confirmed before removing inner catches?

## Related

- [Failure Posture and Defensive Design](../01-concepts/03-failure-posture-and-defensive-design.md)
- [Preserving and Not Swallowing Errors](../01-concepts/04-preserving-and-not-swallowing-errors.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
