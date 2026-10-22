# Fail-Closed vs Fail-Open, Cascades, and Eligibility

> Part XI · Chapter 30 · Sections 30.13–30.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Fallback Failure, Silent Inaccuracy, and Communication](./04-fallback-failure-silent-inaccuracy-and-communication.md)

## In one sentence

**Fail-closed** denies the operation when a check cannot run; **fail-open** allows it — and the choice
must be made per capability from the cost of being wrong, with **eligibility rules** that stop a
fallback from cascading into a second failure.

## Why this matters in production

Fail-open vs fail-closed is a security-shaped decision hiding inside a resilience chapter. An
authorization check that fails open is a breach. A recommendations widget that fails closed is an
outage. Teams often inherit a default from a library or a framework and never revisit it. Worse, they
let fallbacks call each other — cache → replica → primary — so a single failure walks down the chain
until it hits the database. Both problems are solved by writing the rule down per capability.

## 30.13 — Fail closed vs fail open

### Definitions

| Mode | On failure | Preserves | Sacrifices |
| ---- | ---------- | --------- | ---------- |
| **Fail-closed** | Deny / error | Correctness, safety | Availability |
| **Fail-open** | Allow / continue | Availability | Correctness, sometimes safety |

### The core question

```text
If this check cannot run, is it safer to deny or to allow?
  deny  → fail-closed
  allow → fail-open
```

### Common choices

| Capability | Mode | Reason |
| ---------- | ---- | ------ |
| Authentication | Closed | Never trust unverified identity |
| Authorization / permission check | Closed | Never widen access |
| Payment authorization | Closed | Never ship unpaid orders |
| Inventory reservation | Closed | Never oversell |
| Fraud check | Closed (or manual review) | Financial/legal risk |
| Rate limiter | Open or closed? Depends | See below |
| Feature flags | Open to last-known | Stale config is predictable |
| Recommendations | Open (hide) | Optional |
| Analytics | Open (drop) | Non-critical |
| Search personalization | Open (keyword) | Core search still correct |
| Email delivery | Open (queue) | Delay acceptable |
| Session cache | Closed for writes, open for reads? | Depends on revocation |

### The rate-limiter subtlety

A rate limiter that fails closed can become a self-inflicted outage: if its store is down, every
request is rejected. Many systems **fail-open** on limiter errors but keep a local fallback counter.
Security-sensitive limiters (login attempts) may fail closed or use a conservative local limit.

```ts
async function allowRequest(key: string): Promise<boolean> {
  try {
    return await redisLimiter.allow(key);
  } catch {
    // Limiter unavailable: use a conservative in-process token bucket.
    return localLimiter.allow(key);
  }
}
```

The point is not a universal answer; the point is that the answer is **explicit and tested**.

## 30.14 — Avoiding cascading fallbacks

A cascade happens when the fallback for A is B, the fallback for B is C, and each step adds latency and
load — or when a fallback retries the same failing path.

### Anti-pattern

```text
cache miss → read replica → primary DB → cross-region replica
             (replica down)  (overloaded)  (slow)
```

A cache outage becomes a database outage because the "fallback" is an unbounded query storm.

### Rules

1. **A fallback may not depend on the dependency that just failed.**
2. **A fallback may not call the primary path.**
3. **Each step has its own budget**, shrinking down the chain.
4. **The chain has a maximum length** (usually 2–3).
5. **The chain has a terminal state** (`503` or a static value), never a loop.
6. **Skip steps whose breaker is open.**
7. **Do not chain fallbacks for required data** — fail closed instead.

```ts
const chain = [
  { name: "live", run: () => provider.get(), needs: "provider" },
  { name: "cache", run: () => cache.get(), needs: "cache" },
  { name: "static", run: async () => STATIC_DEFAULT, needs: null },
];

async function runChain<T>(steps: Step<T>[], deadline: number): Promise<Sourced<T>> {
  for (const step of steps) {
    if (step.needs && breakers.get(step.needs)?.isOpen()) continue;
    const remaining = deadline - Date.now();
    if (remaining <= 50) break;
    try {
      return { value: await withTimeout(step.run(), Math.min(remaining, 500)),
               source: step.name, asOf: Date.now(), degraded: step.name !== "live" };
    } catch {
      continue; // next step, never the same step
    }
  }
  throw new UnavailableError("ALL_FALLBACKS_EXHAUSTED");
}
```

### Cascade detection

| Signal | Meaning |
| ------ | ------- |
| Fallback latency ≈ primary latency | Chain is not cheaper |
| Multiple `fallback_used_total` parts at once | Common dependency failing |
| DB QPS spike after cache errors | Cache fallback hits DB |
| `ALL_FALLBACKS_EXHAUSTED` rising | Chain is too optimistic |

## 30.15 — Eligibility rules

Not every request should be allowed to use a fallback. **Eligibility** decides *who* and *what* may
degrade.

### Dimensions

| Dimension | Rule example |
| --------- | ------------ |
| **Capability** | Only optional/important features |
| **Tenant** | No fallback for tenants with contractual freshness |
| **Operation** | No fallback for money-moving writes |
| **Data class** | No stale permissions or balances |
| **User role** | Admins see errors, not substitutes |
| **Region** | Fallback only where regulation allows |
| **Time** | No fallback during financial close |
| **Age** | Stale only within tolerance |

```ts
interface FallbackEligibility {
  capability: "required" | "important" | "optional";
  operation: "read" | "write" | "money" | "auth";
  tenant?: { requiresFreshData: boolean };
  dataClass?: "public" | "personal" | "financial" | "security";
}

function mayFallback(e: FallbackEligibility): boolean {
  if (e.capability === "required") return false;
  if (e.operation === "money" || e.operation === "auth") return false;
  if (e.tenant?.requiresFreshData) return false;
  if (e.dataClass === "financial" || e.dataClass === "security") return false;
  return true;
}
```

### Default deny

Eligibility should default to **no fallback** and require an explicit opt-in per capability. This
prevents a new endpoint from inheriting a silent default just because it reuses a helper.

```ts
const policy = fallbackPolicy.for("recommendations"); // explicit registration
if (!policy || !mayFallback(policy.eligibility)) throw new UnavailableError();
```

## Worked example — permissions cache

Acme cached permission checks for 30s. During a Redis outage, the natural fallback was "use the last
cached value." That is **fail-open** and unacceptable: a revoked user could retain access.

```text
capability: authorization     → required
operation:  auth              → not eligible
dataClass:  security          → not eligible
decision:   fail closed, recompute from primary DB with a strict timeout
```

The team added a local, short-lived (5s) permission cache as the only fallback, and only for *reads*
of a user's own permissions — never for cross-tenant checks. Redis outages now cause a modest latency
increase, not an access-control gap.

## Key data / numbers

- Fallback chain length: **2–3** steps maximum.
- Per-step fallback budget: **≤ 500ms**, shrinking down the chain.
- Cache fallback for security data: **0** (fail closed).
- Local limiter fallback: conservative, e.g. **50%** of the normal rate.
- Hysteresis before leaving degraded mode: **2×** breaker cooldown.
- Eligibility review: on every new endpoint/capability.

## Real-world use case — Acme SaaS

Acme's API gateway failed open on its rate limiter during a Redis incident. A single misbehaving
tenant sent 40× normal traffic and saturated the database. The postmortem kept fail-open (rejecting all
traffic would have been worse) but added a local token bucket at 40% of the normal limit, per-tenant
caps, and an alert when the limiter store was unavailable. A repeat incident produced a 2× traffic
increase instead of 40×, and no database saturation.

## Trade-offs

| Choice | Benefit | Cost |
| ------ | ------- | ---- |
| Fail-closed auth/payments | Safety | Availability |
| Fail-open optional features | Availability | Some incorrect UX |
| Long fallback chains | Higher hit rate | Latency, cascade risk |
| Strict eligibility | Safety | More errors during incidents |
| Default deny | Prevents accidents | More explicit registration |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide per capability | Use a global default |
| Fail closed for auth, money, security | Fall back to stale permissions |
| Fail open for optional features | Hide required failures |
| Cap chain length | Let fallbacks recurse |
| Skip steps with open breakers | Try every step blindly |
| Default eligibility to deny | Inherit fallbacks implicitly |
| Test the chain under fault injection | Assume it terminates |

## Common mistakes

- **A single `failOpen` flag** for the whole service.
- **Fallback to stale permissions**, a security hole.
- **Chains that end in the primary DB**, causing a second outage.
- **No terminal state**, so a request retries fallbacks forever.
- **Eligibility checked after the fallback runs**, too late.

## Checklist

- [ ] Each capability has an explicit fail-open/closed decision.
- [ ] Auth, money, and security data fail closed.
- [ ] Optional features degrade rather than error.
- [ ] Fallback chains are ≤ 3 steps with shrinking budgets.
- [ ] No fallback calls the primary or the failed dependency.
- [ ] Chains have a terminal `ALL_FALLBACKS_EXHAUSTED` state.
- [ ] Eligibility defaults to deny and is tested.

## Related

- [Fail-Open vs Fail-Closed](../02-deep-dive/02-fail-open-vs-closed.md)
- [Fallback Chains](../02-deep-dive/01-fallback-chains.md)
- [Principles of Graceful Degradation](./01-principles-and-required-vs-optional.md)
- [Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
