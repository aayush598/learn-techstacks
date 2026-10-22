# Entitlement Resolution and Quota Mechanics

> Part XVI · Chapter 42 · Sections 42.11, 42.12 · _Estimated reading time: 20 min_
> **Prerequisite:** [Refunds, Subscription States, Quotas, and Entitlements](../01-concepts/03-refunds-subscription-states-and-entitlements.md)

## In one sentence

Quota counters must be consumed **atomically in the store**, and entitlement lookups must
distinguish **"not entitled" (deny)** from **"cannot verify" (policy decision)** — because
collapsing those two turns a five-minute cache outage into a customer-visible outage.

## Why this matters in production

Two failure shapes dominate real incidents here. First, the **read-modify-write race**: two
concurrent requests read `used = 99`, both write `100`, and the monthly quota of 100 becomes
102 — multiplied across tenants, that is a real cost overrun on compute-heavy features.
Second, the **collapsed 403**: the entitlement service times out, the handler throws a generic
"forbidden," and the client caches it — users stay locked out long after the service
recovers, even though their plan was fine. Both are fixed by mechanics, not by more try/catch.

## Atomic quota consumption

Never compute `new = used + n` in application code. Push the check-and-increment into one
atomic operation:

```sql
-- Single-statement hard cap: the UPDATE's WHERE clause IS the check.
INSERT INTO quota_usage (tenant_id, window_start, used)
VALUES ($1, date_trunc('month', now()), $2)
ON CONFLICT (tenant_id, window_start)
DO UPDATE SET used = quota_usage.used + $2
WHERE quota_usage.used + $2 <= $3        -- $3 = plan limit
RETURNING used;
-- 0 rows returned ⇒ over quota. No race window exists.
```

Or, for Redis-backed counters, a Lua script so check-and-decrement is atomic:

```lua
-- KEYS[1]=quota:{tenant}:{window}  ARGV[1]=limit  ARGV[2]=cost
local used = tonumber(redis.call("GET", KEYS[1]) or "0")
if used + tonumber(ARGV[2]) > tonumber(ARGV[1]) then
  return nil                            -- over quota; caller emits 429/402
end
redis.call("INCRBY", KEYS[1], ARGV[2])
redis.call("EXPIRE", KEYS[1], 2592000) -- safety TTL ~30 days; window key owns truth
return used + tonumber(ARGV[2])
```

**Key data:** window strategies — **fixed window** (simple, allows a 2× burst at the
boundary), **sliding window/log** (accurate, more state), **token bucket** (smooth rate,
commonly used for per-second rate limits). Choose fixed-window for monthly plan quotas
(burst risk is acceptable), sliding/token-bucket for rate limits users can hit in a burst.
Always set a safety TTL on counter keys so a lost reset cannot leak memory forever.

## What happens when the counter store is down

This is a policy decision, recorded in code, not an unhandled exception:

| Operation class | Policy | Rationale |
| --------------- | ------ | --------- |
| Cheap read | Fail-open from cache, else closed | Overuse of reads is survivable |
| Metered compute (exports, LLM calls, renders) | **Fail-closed** | Cost is real and immediate |
| Irreversible external action (send email, charge) | **Fail-closed** | Abuse window is dangerous |
| First request in a cold window | Fail-closed unless cached last-known | Default to safe |

```ts
async function consumeQuota(tenantId: string, op: MeteredOp): Promise<void> {
  try {
    const used = await redis.eval(CONSUME_LUA, [key(tenantId, op.window)],
      [op.limit, op.cost]);
    if (used === null) throw new QuotaExceeded({ op: op.name, limit: op.limit }); // 402/429
  } catch (err) {
    if (!isStoreUnavailable(err)) throw err;
    // Store down: policy per operation class — never a generic 500.
    if (op.class === "cheap_read") {
      const cached = await cache.getOrThrow(`quota_snapshot:${tenantId}:${op.name}`);
      if (cached.remaining >= op.cost) return;   // degraded but bounded
    }
    throw new QuotaUnverifiable({ op: op.name }); // 503-class: "try again shortly"
  }
}
```

**Key data:** the error contract matters as much as the policy — `429/402 QUOTA_EXCEEDED`
(plan-limited, purchase CTA) vs `503 QUOTA_UNVERIFIABLE` (store down, retry shortly). Clients
must not treat the second as a plan limit; support must not either.

## Entitlement resolution path

```text
request ──▶ assertEntitlement(tenant, feature)
                │
                ├─1─▶ cache (TTL 1–5 min, invalidated by billing outbox events)
                │         hit ──▶ granted / denied
                ├─2─▶ entitlement service (projection of subscriptions + manual grants)
                │         ok  ──▶ populate cache ──▶ granted / denied
                │         down ──▶ 3
                └─3─▶ policy: last-known snapshot? fail-open? fail-closed?
                          └─▶ granted (degraded) | EntitlementUnverifiable (503)
```

Failure modes at each hop:

| Hop | Failure | Handling |
| --- | ------- | -------- |
| Cache miss + service down | Outage | Last-known snapshot, then per-feature policy |
| Service returns denied, but billing webhook says upgraded seconds ago | Stale projection | Short TTL + outbox-driven invalidation shrinks the window; UI can show "upgrading…" |
| Manual grant/override in admin | Bypasses projection | Apply as an overlay with its own expiry, audited |
| Feature not in the entitlement matrix (new code, old data) | Unknown feature | Deny by default + metric; unknown ≠ free |

**Key data:** recommended cache TTL **1–5 minutes** for money-adjacent features, with the
billing outbox event (`subscription.changed`) invalidating immediately on transition —
practically, upgrade latency then becomes "webhook latency + one cache hop," commonly
seconds. Manual overrides should carry an explicit `expires_at`; permanent silent overrides
are how "test grant" ends up in production billing.

## Real-world use case — Acme's export quota outage

Acme metered `ExportJob` per tenant with a Redis counter and a `try/catch` that mapped every
error to `403 QUOTA_EXCEEDED`. During a Redis failover (~6 minutes), every export in the
product returned `403`; the frontend logged users out "to refresh permissions," and support
tickets spiked. Analysis: the entitlement itself was fine — only the *counter* was
unverifiable. The fix separated the two errors (`QUOTA_EXCEEDED` vs `QUOTA_UNVERIFIABLE`),
made the export path fail-closed with a `503` + `Retry-After: 30` and a clear "billing system
briefly unavailable, your plan is unaffected" message, and added a cached last-known snapshot
(5-minute TTL) that let ~80% of export attempts through during the next failover. Outage
became a non-event.

## Trade-offs

| Decision | Option A | Option B | Pick when |
| -------- | --------- | -------- | --------- |
| Counter location | Redis (fast, ephemeral) | Postgres (durable, slower) | Redis + snapshot for rates; Postgres for billing-grade monthly quotas |
| Store-down posture | Fail-open | Fail-closed | Cost/abuse risk ⇒ closed; pure reads ⇒ open |
| Window type | Fixed (cheap) | Sliding (accurate) | Monthly caps ⇒ fixed; bursty rate limits ⇒ sliding |
| Cache TTL | Long (cheap) | Short (fresh) | Money-adjacent ⇒ short + event invalidation |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check-and-increment in one SQL/Lua operation | `get` then `set` in app code |
| Separate "exceeded" from "unverifiable" errors | Map store outages to 403 |
| Default-unknown features to denied | Default to free |
| Give manual grants an expiry + audit row | Leave permanent test grants |
| Set safety TTLs on counter keys | Trust resets that may never run |

## Common mistakes

- **Two-step quota checks** — the race is small until launch day, then it is your invoice.
- **Unbounded fail-open** — an outage becomes a free-compute window for every tenant.
- **Caching denials aggressively** — a resolved upgrade keeps denying for the cache TTL.
- **Entitlement = feature flag** — flags gate rollout; entitlements grant rights; mixing them
  makes both unauditable.
- **No metric on `unverifiable`** — silent policy decisions are invisible until a customer
  notices.

## Checklist

- [ ] Quota consumption is a single atomic operation in the store.
- [ ] `QUOTA_EXCEEDED` and `QUOTA_UNVERIFIABLE` are distinct codes with distinct HTTP classes.
- [ ] Per-operation-class fail-open/closed policy is written down next to the code.
- [ ] Entitlement cache TTL is short and billing events invalidate it.
- [ ] Unknown features fail closed and emit a metric.
- [ ] Manual grants are expiring and audited.

## Related

- [Refunds, Subscription States, Quotas, and Entitlements](../01-concepts/03-refunds-subscription-states-and-entitlements.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Part XV — Advanced Distributed-System Failure Handling](../../../part-15-distributed-failures/README.md)
- [Chapter 42 Reference](../05-reference/README.md)
