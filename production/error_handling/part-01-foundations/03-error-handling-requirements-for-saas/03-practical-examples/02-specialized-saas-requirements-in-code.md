# Specialized SaaS Requirements in Code

> Part I · Chapter 3 · Sections 3.4–3.9 · _Estimated reading time: 26 min_

## In one sentence

Each specialized profile — multi-tenant, high-availability, financial, AI, real-time, background —
turns into a **specific line of code or configuration** that you either have or do not.

## Why this matters in production

"Be multi-tenant" and "be reliable" are slogans until they become code. This file expresses each
profile's obligation as a concrete, reviewable artifact, so you can audit your product profile by
profile instead of hoping the requirements are met.

## 3.4 Multi-tenant — scoping and fair share

```ts
// Obligation: tenant derived from session; scoped query; per-tenant limit.
async function listDocuments(principal: Principal, limit = 50) {
  const ok = await quota.tryConsume(principal.tenantId, "docs:list", 1);
  if (!ok) throw new RateLimited({ tenantId: principal.tenantId, retryAfterSeconds: 30 });
  return db.query(
    "SELECT id, title FROM documents WHERE tenant_id = $1 LIMIT $2",
    [principal.tenantId, limit],                       // session tenant, never request body
  );
}
```

**Key data:** `429` + `Retry-After`; scoped `404` (not `403`) on misses; cache/queue keys prefixed
with `tenantId`.

## 3.5 High-availability — timeouts, breakers, degradation

```ts
// Obligation: every external call bounded; optional dep degrades; critical dep fails fast.
const llm = new Client({ timeoutMs: 8_000, breaker: { failures: 5, cooldownMs: 30_000 } });

async function renderPage(principal: Principal) {
  const core = await coreData.fetch(principal);        // critical → throws → 503 at boundary
  let summary: string | null = null;
  try { summary = await llm.summarize(core.text); }
  catch (err) { log.warn({ err }, "summary degraded"); } // optional → degrade honestly
  return { core, summary, degraded: summary === null };
}
```

**Key data:** timeout < caller budget; breaker opens after ~5 failures; `503` + `Retry-After` for
critical dependency down; `200` with a degraded marker for optional.

## 3.6 Financial — idempotency, compensation, audit

```python
# Obligation: idempotent charge; compensate on later-step failure; append-only audit.
def checkout(order, idempotency_key):
    charge = payments.charge(order.amount, idempotency_key=idempotency_key)  # no dup charge
    audit.append({"event": "charged", "order": order.id, "charge": charge.id})

    reservation = None
    try:
        reservation = inventory.reserve(order.items)                        # step 2
    except InventoryUnavailable as e:
        payments.refund(charge.id, idempotency_key=f"refund:{charge.id}")   # compensate step 1
        audit.append({"event": "compensated", "charge": charge.id})
        return Err(OrderFailed(reason="inventory", cause=e))
    return Ok(Order(id=order.id, charge=charge.id, reservation=reservation.id))
```

**Key data:** Stripe idempotency TTL 24h; SQLSTATE `40001` retryable; refund uses its own key;
audit is append-only.

## 3.7 AI-powered — provider abstraction, limits, fallback

```ts
// Obligation: classify provider vs app errors; bound cost/time; honest fallback.
async function runAgent(prompt: string) {
  try {
    return await provider.complete(prompt, { maxTokens: 1_500, timeoutMs: 15_000 });
  } catch (err) {
    if (err instanceof ProviderRateLimit) {                 // 429 → transient
      return withRetry(() => provider.complete(prompt), { attempts: 3 });
    }
    if (err instanceof ProviderTimeout) {                   // try fallback model
      try { return await fallback.complete(prompt); }
      catch (e2) { throw new AgentUnavailable({ cause: e2 }); }
    }
    throw err;                                              // app bug → fail-fast
  }
}
```

**Key data:** provider `429` + `Retry-After`; token caps; distinct codes for provider vs tool vs app;
never present fallback content as authoritative.

## 3.8 Real-time — deadlines, backpressure, resume

```ts
// Obligation: deadline propagation; reject when saturated; resume via sequence numbers.
async function handleLiveUpdate(conn: Connection, event: LiveEvent) {
  if (!conn.withinDeadline()) return;                        // a late result is a failure
  if (conn.outbox.full()) {                                   // backpressure
    conn.coalesce(event);                                    // keep latest, drop redundant
    return;
  }
  try {
    await conn.send(event, { seq: event.seq });              // client dedups/resumes on seq
  } catch (err) {
    return conn.scheduleReconnect({ resumeFrom: event.seq }); // at-least-once + resume
  }
}
```

**Key data:** end-to-end deadline; drop/coalesce rather than stall; sequence numbers for
dedup/resume; explicit reconnect.

## 3.9 Background — retries, DLQ, checkpoints

```go
// Obligation: bounded retries, DLQ with context, checkpoint for resume, idempotent processing.
func (j *ExportJob) Process(ctx context.Context, msg Message) error {
    cp, _ := j.checkpoints.Load(msg.JobID)          // resume point
    for _, page := range j.pages(msg, cp) {
        if err := j.writeIdempotent(page, msg.JobID); err != nil {
            return err                              // caller retries with backoff; DLQ after max
        }
        j.checkpoints.Save(msg.JobID, page.Cursor)  // checkpoint after each page
    }
    return nil
}
```

**Key data:** max attempts commonly 5; backoff with jitter; DLQ preserves job ID + last error +
cursor; writes idempotent via a deterministic key.

## Key data / numbers — master table

| Profile | Concrete artifact | Key value |
| ------- | ----------------- | --------- |
| Multi-tenant | Scoped query + quota check | `tenant_id` from session; `429` |
| High-availability | Timeout + breaker + degrade | timeout < budget; open after ~5 |
| Financial | Idempotent charge + compensate + audit | key TTL 24h; `40001` retryable |
| AI | Provider abstraction + limits | `429`/`Retry-After`; token cap |
| Real-time | Deadline + backpressure + seq | drop/coalesce; resume from seq |
| Background | Retry + DLQ + checkpoint + idempotent | max 5; DLQ context |

## Real-world use case — Acme SaaS

Acme's `Checkout` (financial) and `ExportJob` (background) shared a retry utility. When a payment
retry was added to the export workflow "for consistency," the utility retried a **non-idempotent**
inventory reservation, creating duplicate holds. The root cause: requirements differ by profile —
background retries assume idempotent writes, financial retries require keys. The fix separated the
two: `ExportJob` got checkpoint + idempotent keys; `Checkout` got idempotency keys + compensation.
One utility could not satisfy two profiles, and pretending it could was the bug.

## Trade-offs

| Profile obligation | Cost | Failure if skipped |
| ------------------ | ---- | ------------------ |
| Tenant scoping | Low | Data breach |
| Timeouts/breakers | Low–medium | Cascading outage |
| Idempotency + compensation | Medium | Double charges / inconsistency |
| Provider abstraction | Medium | Cost runaway / coupling |
| Deadline + backpressure | Medium | Stale data / stall |
| DLQ + checkpoint | Medium | Poison message / lost job |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Express each profile as a concrete artifact | Rely on slogans |
| Derive tenant from the session | Trust the request body |
| Make money ops idempotent + compensable | Retry money without keys |
| Bound AI cost/time | Run LLMs unbounded |
| Checkpoint long jobs | Restart from scratch after failure |

## Common mistakes

- **One retry utility for all profiles** — ignores idempotency differences.
- **Unscoped cache keys** — cross-tenant leakage.
- **LLM fallback presented as fact.**
- **Real-time results delivered late as success.**
- **Background jobs without a DLQ.**

## Checklist

- [ ] Is every profile obligation a line of code or config?
- [ ] Are money operations idempotent and compensable?
- [ ] Are AI calls bounded in tokens, time, and cost?
- [ ] Do real-time paths enforce deadlines and backpressure?
- [ ] Do background jobs checkpoint and DLQ?

## Related

- [Requirements by Architecture and Risk Profile](../01-concepts/02-requirements-by-architecture-and-risk-profile.md)
- [Multi-Tenancy, Isolation, and High Availability — Deep Dive](../02-deep-dive/01-multi-tenancy-isolation-and-high-availability.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
