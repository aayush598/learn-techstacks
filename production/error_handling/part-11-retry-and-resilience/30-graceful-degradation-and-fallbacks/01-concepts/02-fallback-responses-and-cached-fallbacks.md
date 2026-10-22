# Fallback Responses and Cached Fallbacks

> Part XI · Chapter 30 · Sections 30.3–30.5 · _Estimated reading time: 19 min_
> **Prerequisite:** [Principles of Graceful Degradation](./01-principles-and-required-vs-optional.md)

## In one sentence

A fallback response is a **pre-approved substitute** for a failed call — computed, cached, or static —
and it is only graceful if it is correct for the moment and honest about being a substitute.

## Why this matters in production

Most "graceful degradation" bugs are not crashes; they are fallbacks that quietly return the wrong
thing. A cached balance shown as live, an empty recommendation list that looks like "no results," a
default shipping rate that undercharges — each is availability won at the cost of correctness. The
skill is choosing the right substitute and encoding enough metadata that nobody downstream mistakes it
for the real thing.

## 30.3 — Fallback responses

### Categories

| Type | Example | Risk | Use when |
| ---- | ------- | ---- | -------- |
| **Cached** | Last known exchange rate | Staleness | Read-heavy, tolerant of age |
| **Computed/default** | Flat shipping estimate | Inaccuracy | Value is an estimate by nature |
| **Degraded real** | Search without personalization | Reduced quality | Core result still correct |
| **Static/template** | Generic LLM summary | Generic | Content is optional |
| **Empty/omit** | Hide recommendations | Looks like "none" | Absence is unambiguous |
| **Queued/later** | Send receipt later | Delay | Async side effect |
| **Explicit error** | `503` + `Retry-After` | None | No correct substitute exists |

### Rules for a fallback response

1. **Correct for the contract.** The shape must satisfy the schema; optional fields may be absent.
2. **Labelled.** Include `degraded: true`, a `source`, and the fallback's own timestamp.
3. **Bounded.** It must not call another unbounded dependency.
4. **Cheap.** A fallback should be faster than the primary path, not slower.
5. **Reversible.** Remove the fallback when the dependency recovers.

```json
{
  "items": [],
  "degraded": true,
  "degraded_reason": "recommendations_unavailable",
  "source": "cache",
  "as_of": "2026-10-21T09:12:00Z",
  "notice": "Personalized recommendations are temporarily unavailable."
}
```

### The empty-result trap

An empty list is ambiguous: it can mean "none" or "failed." If the UI cannot distinguish them, add a
flag or a notice. For required data, prefer an error over an empty list.

## 30.4 — Cached fallbacks

A cached fallback serves the last successful value when the live source fails.

```ts
interface Cached<T> { value: T; at: number; }

class CachedFallback<T> {
  constructor(
    private readonly maxStaleMs: number,
    private readonly store: { get(k: string): Promise<Cached<T> | null> },
    private readonly key: string,
  ) {}

  async get(live: () => Promise<T>): Promise<{ value: T; stale: boolean; ageMs: number }> {
    try {
      const value = await live();
      return { value, stale: false, ageMs: 0 };
    } catch (err) {
      const cached = await this.store.get(this.key);
      if (!cached) throw err;
      const ageMs = Date.now() - cached.at;
      if (ageMs > this.maxStaleMs) throw err;
      return { value: cached.value, stale: true, ageMs };
    }
  }
}
```

### Cache design questions

| Question | Why it matters |
| -------- | -------------- |
| What is the maximum acceptable age? | Beyond it, data is misleading |
| Is the value monotonic or time-sensitive? | Prices/balances change fast |
| Is the cache shared or per-instance? | Per-instance misses on cold start |
| How is the cache populated? | Only on success, never on failure |
| Can a stale value be harmful? | Permissions and money usually yes |

> ⚠️ **Hazard.** Never populate a fallback cache from a degraded path. Otherwise one bad response
> becomes the "last known good" value for every subsequent failure.

### HTTP cache semantics

```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=30, stale-if-error=300
Age: 47
Warning: 110 - "Response is stale"
X-Degraded: cache
```

`stale-if-error` lets a CDN or shared cache serve stale content during an origin error. Use it for
public, non-personalized content, and **never** for balances, permissions, or prices unless the
contract explicitly allows estimates.

## 30.5 — Stale vs unavailable

"Stale" and "unavailable" are different states and need different handling.

| State | Meaning | Response | UI |
| ----- | ------- | -------- | -- |
| **Fresh** | Live, within TTL | Normal | Normal |
| **Stale** | Cached, beyond freshness but within tolerance | `200` + `Warning`/`X-Degraded` | "Updated 2h ago" |
| **Unavailable** | No acceptable value | `503`/`404` | "Temporarily unavailable" |

### Freshness budget

```text
freshness window:  0–60s    → fresh
tolerance window:  60s–24h  → stale, serve with label (for suitable data)
beyond tolerance:  >24h     → unavailable
```

The tolerance depends on the data: a shipping ETA can be hours stale; an account balance cannot.

```ts
function present(cached: Cached<Balance>) {
  const age = Date.now() - cached.at;
  if (age <= 60_000) return { state: "fresh" as const, ...cached };
  if (age <= 300_000) return { state: "stale" as const, ...cached };
  throw new UnavailableError("BALANCE_TOO_STALE");
}
```

## Worked example — exchange rate

```text
primary: rates.provider.com (p99 400ms)
cache:   Redis, TTL 60s, tolerance 6h

t=0     live call succeeds, store {rate, at}
t=60    cache technically stale; live still used and refreshed
t=61    provider times out; serve cached rate (age 61s) with stale=true
t=6h1m  provider still down; age > tolerance → 503 "rate unavailable"
```

Acme uses the stale rate for **display** on the pricing page with "indicative rate" copy, but checkout
recomputes the charge from the live provider and fails closed if it cannot.

## Key data / numbers

- Default freshness: **30–60s** for volatile data; **minutes–hours** for reference data.
- Stale tolerance: **minutes** for balances, **hours** for ETAs/rates display, **days** for content.
- Fallback budget: ≤ **20%** of the user deadline.
- Cache populated **only on success**.
- `stale-if-error`: **300s** typical for public content; not for personalized/monetary data.
- Degraded marker: `X-Degraded` or a `degraded` body field.

## Real-world use case — Acme SaaS

Acme's pricing page called a currency API synchronously. During a provider outage the page returned
`500`, and the marketing team lost signups for 40 minutes. The team added a Redis cache (60s TTL, 6h
tolerance) and a stale-labelled response. The next outage served indicative rates with "rates delayed"
copy within 80ms, and the signup form stayed available. Checkout was untouched because it never trusted
the display rate — it charged from the payment provider's own conversion and failed closed if that was
unavailable.

## Trade-offs

| Option | Availability | Correctness | Complexity |
| ------ | ------------ | ----------- | ---------- |
| Fail immediately | Low | High | Low |
| Cached stale | High | Medium | Medium |
| Static default | High | Low | Low |
| Degraded real | High | High-ish | High |
| Queued/later | High | Delayed | Medium |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Label stale responses | Present stale data as live |
| Bound stale tolerance per data type | Use one TTL for everything |
| Populate cache only on success | Cache degraded responses |
| Return an explicit error when no value is acceptable | Return an empty or zero value |
| Make fallbacks cheap | Call the primary from the fallback |
| Show the data's age | Show only "updated recently" |

## Common mistakes

- **Empty array as a fallback**, indistinguishable from a valid empty result.
- **Zero/`null` monetary values**, silently undercharging or misreporting.
- **Infinite stale tolerance**, serving week-old data indefinitely.
- **Caching a fallback**, poisoning the cache.
- **Stale personalized data**, leaking another user's cached response (see Chapter 34).

## Checklist

- [ ] Every fallback names its type and source.
- [ ] Responses carry a degraded marker and `as_of`.
- [ ] Stale tolerance is set per data type.
- [ ] Cache is written only on success.
- [ ] No fallback calls the primary recursively.
- [ ] Empty results are distinguishable from failures.
- [ ] Monetary/permission data fails closed when stale.

## Related

- [Partial Features, Degraded Mode, and Disabling](./03-partial-features-degraded-mode-and-disabling.md)
- [Fallback Chains](../02-deep-dive/01-fallback-chains.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Chapter 30 Reference](../05-reference/README.md)
