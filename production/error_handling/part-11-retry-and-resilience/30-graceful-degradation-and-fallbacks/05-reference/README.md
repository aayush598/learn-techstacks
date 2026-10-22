# Chapter 30 — Reference

> Part XI · Chapter 30 · All sections

Quick-reference material for graceful degradation. Pair this with [Do's and Don'ts](../04-dos-and-donts/README.md)
and the [Chapter 29 reference](../../29-timeouts-circuit-breakers-and-bulkheads/05-reference/README.md).

## Required vs optional

| Class | Core task possible? | Correct without dependency? | Behavior |
| ----- | :-----------------: | :-------------------------: | -------- |
| Required | No | No | Fail closed |
| Important | Yes | No (degraded quality) | Degrade + visible notice |
| Optional | Yes | Yes | Hide/label |
| Decorative | Yes | Yes | Omit silently |

## Fallback type selection

| Data characteristic | Preferred fallback |
| ------------------- | ------------------ |
| Volatile, display-only | Cached with age label |
| Volatile, monetary | None — fail closed |
| Reference data | Cached, long tolerance |
| Optional content | Static/template |
| Optional list | Omit with notice |
| Async side effect | Queue and retry |
| Permission/security | None — fail closed |
| Search | Keyword-only |
| LLM output | Smaller model → extractive → template |

## Stale tolerance

| Dataset | Fresh | Stale (labelled) | Unavailable |
| ------- | ----- | ---------------- | ----------- |
| Exchange rate (display) | 60s | ≤ 6h | > 6h |
| Shipping ETA | 5min | ≤ 1h | > 1h |
| Product catalog | 1min | ≤ 1h | > 1h |
| Account balance | 5s | never | immediately |
| Permissions | 0–5s local | never cross-tenant | immediately |
| Usage charts | 5min | ≤ 24h | > 24h |
| LLM summary | 24h cache | marked "saved" | template |

## Degraded-mode matrix template

| Level | Name | Trigger | Checkout | Auth | Search | Exports | Optional |
| :---: | ---- | ------- | :------: | :--: | :----: | :-----: | :------: |
| 0 | Normal | All healthy | on | on | on | on | on |
| 1 | Reduced | Optional dep down / util > 85% | on | on | reduced | on | off |
| 2 | Essential | Important dep down | on | on | reduced | deferred | off |
| 3 | Read-only | Primary writer down | readonly | on | reduced | off | off |
| 4 | Unavailable | Auth or primary DB down | off | off | off | off | off |

## Fail-open vs fail-closed

```text
Does proceeding without the check produce an incorrect or unsafe result?
├─ Yes → fail closed
└─ No  → can the effect be reversed or compensated?
          ├─ No  → fail closed
          └─ Yes → will the fallback be counted and alerted?
                    ├─ No  → add instrumentation first (treat as closed)
                    └─ Yes → fail open, labelled
```

| Capability | Mode |
| ---------- | ---- |
| Authentication | Closed |
| Authorization / tenant isolation | Closed |
| Payment authorization | Closed |
| Inventory reservation | Closed |
| Tax charge | Closed |
| Idempotency check | Closed |
| Recommendations | Open (hide) |
| Search personalization | Open (keyword) |
| LLM summary | Open (chain) |
| Email receipt | Open (queue) |
| Analytics | Open (drop, count) |
| Feature flags | Last-known cache |
| Rate limiter | Open + local limit |

## Eligibility rules

A fallback is allowed only if **all** hold:

1. Capability is `important` or `optional`.
2. Operation is not money-moving or auth.
3. Tenant does not require fresh data by contract.
4. Data class is not `financial` or `security`.
5. A correct substitute exists.
6. The substitute has a budget and cannot reach the failed dependency.
7. The result will be labelled.

Default is **deny**; capabilities opt in explicitly.

## Fallback chain rules

```text
length ≤ 3 (4 with a static terminal)
shared deadline, safety 50–200ms
later steps get smaller budgets
skip step if breaker open or remaining < minUseful
never call the primary from a fallback
terminal state: ALL_FALLBACKS_EXHAUSTED
provenance: source, asOf, degraded
```

## API conventions

### Headers

| Header | Value | Notes |
| ------ | ----- | ----- |
| `X-Degraded` | comma-separated parts or `true` | Machine-readable |
| `X-Degraded-Mode` | `0`–`4` | System level |
| `X-Degraded-Reason` | `dependency_unavailable` | No internal details |
| `X-Data-Source` | `live`/`cache`/`derived`/`static` | Per response |
| `X-Data-As-Of` | ISO 8601 | Age of the data |
| `Warning` | `199`/`110` | Human/proxy hint |
| `Retry-After` | seconds | On `503`/`429` |

### Body

```json
{
  "data": {},
  "degraded": true,
  "degraded_parts": ["recommendations"],
  "source": "cache",
  "as_of": "2026-10-21T09:12:00Z",
  "notice": "Some features are temporarily limited."
}
```

### Status codes

| Situation | Status |
| --------- | ------ |
| Degraded but correct | `200` + degraded headers |
| Deferred async work | `202` + job location |
| Feature disabled (level) | `503` + `Retry-After` |
| No acceptable data | `503` |
| Required resource missing | `404` |
| Read-only mode write | `503` + `READ_ONLY_MODE` |
| Client disconnected | `499` (internal only) |

## User-facing copy

| State | Copy |
| ----- | ---- |
| Stale data | "Updated 2 hours ago" |
| Reduced search | "Showing basic results" |
| Feature off | "Temporarily unavailable" |
| Deferred job | "We'll notify you when it's ready" |
| Read-only | "Changes are temporarily unavailable" |
| Maintenance | "We'll be back shortly" |

Avoid: "Live", "Real-time", "All systems normal", "No results" when the truth is "we couldn't ask."

## Metrics

```text
degraded_mode{level}
degraded_requests_total{level,feature}
fallback_used_total{dependency,fallback}
fallback_failed_total{dependency,fallback}
summary_source_total{source}
stale_served_total{dataset,age_bucket}
deferred_jobs_total{type}
readonly_rejections_total{route}
```

## Testing matrix

| Scenario | Expected |
| -------- | -------- |
| Primary fails | Next step, `degraded=true` |
| Fallback fails | Terminal error, not default value |
| Breaker open for step | Step skipped |
| Deadline nearly expired | Remaining steps skipped |
| Cache stale beyond tolerance | Cache step skipped |
| Flags unavailable | Last-known values |
| Level 3 write | `503 READ_ONLY_MODE` |
| Level 4 | Maintenance response |
| Template output | Clearly labelled, not "AI" |

## Review questions

1. Which capabilities are required, and do they fail closed?
2. What substitute exists for each optional capability?
3. How stale may each dataset be, and is it labelled?
4. What is the chain's worst-case latency?
5. Can any fallback reach the dependency that just failed?
6. Is every fail-open path counted and alerted?
7. Does the mode appear on every surface?
8. Has every degraded path been exercised in staging?
9. Are eligibility rules explicit, or inherited by default?
10. What user decision could be wrong because of this degradation?

## Related

- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../../GLOSSARY.md)
