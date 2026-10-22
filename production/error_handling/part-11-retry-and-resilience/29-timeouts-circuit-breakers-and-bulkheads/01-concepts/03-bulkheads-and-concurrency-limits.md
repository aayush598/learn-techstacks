# Bulkheads and Concurrency Limits

> Part XI · Chapter 29 · Sections 29.10–29.12 · _Estimated reading time: 18 min_
> **Prerequisite:** [Circuit Breaker States and Conditions](./02-circuit-breaker-states-and-conditions.md)

## In one sentence

A **bulkhead** partitions resources — connection pools, worker pools, concurrency slots — by
dependency or tenant, so that one failing or noisy consumer cannot exhaust the capacity everyone
shares.

## Why this matters in production

Timeouts and breakers protect you from a *slow* dependency. Bulkheads protect you from a *greedy*
one. A single endpoint that opens 200 concurrent requests to a slow provider can consume the shared
HTTP pool, and suddenly unrelated endpoints cannot reach healthy services. A single tenant running a
large export can fill the worker queue and delay every other tenant. Bulkheads make the blast radius
of greed and slowness match the thing that caused it.

## 29.10 — Bulkhead isolation

The name comes from ship compartments: a breach floods one compartment, not the hull.

```text
Shared pool (no bulkhead):
  [ req A ][ req B ][ export ][ req C ][ req D ][ export ][ req E ][ export ]
  └────────────── one slow workload starves everyone ──────────────┘

Bulkheads:
  API pool:      [ req A ][ req B ][ req C ][ req D ]
  Export pool:   [ export ][ export ][ export ]   ← capped, isolated
  Provider pool: [ call ][ call ][ call ]         ← capped per dependency
```

### What to partition

| Dimension | Example |
| --------- | ------- |
| **Dependency** | Separate pools for Stripe, S3, LLM |
| **Tenant** | Per-tenant concurrency or rate limit |
| **Workload type** | Interactive vs batch/export |
| **Priority** | Critical checkout vs background sync |
| **Region** | Per-region pools |

Partition the dimension with the highest risk of noisy-neighbor effects. Usually that is dependency
and tenant.

## 29.11 — Concurrency limits

A concurrency limit caps in-flight calls. It is the simplest bulkhead.

```ts
class Semaphore {
  private inFlight = 0;
  private waiters: Array<() => void> = [];

  constructor(private readonly limit: number) {}

  async acquire(signal?: AbortSignal): Promise<() => void> {
    if (this.inFlight >= this.limit) {
      await new Promise<void>((resolve, reject) => {
        const onAbort = () => reject(new Error("acquire aborted"));
        signal?.addEventListener("abort", onAbort, { once: true });
        this.waiters.push(() => {
          signal?.removeEventListener("abort", onAbort);
          resolve();
        });
      });
    }
    this.inFlight++;
    let released = false;
    return () => {
      if (released) return;
      released = true;
      this.inFlight--;
      this.waiters.shift()?.();
    };
  }
}

const stripeSlots = new Semaphore(20);

async function charge(input: ChargeInput) {
  const release = await stripeSlots.acquire();
  try {
    return await stripe.charges.create(input);
  } finally {
    release();
  }
}
```

### Choosing a limit

| Input | How to use it |
| ----- | ------------- |
| Provider rate limit | `limit ≤ allowed_rps × p99_latency` (Little's Law) |
| Pool size | Do not exceed the pool; leave headroom |
| Downstream capacity | Coordinate with the dependency owner |
| Latency SLO | Lower concurrency reduces queueing |

Little's Law: `concurrency ≈ throughput × latency`. If a provider allows 100 req/s and calls take
200ms, then `100 × 0.2 = 20` concurrent calls saturate it.

### Per-tenant limits

```ts
const tenantSlots = new Map<string, Semaphore>();

function slotsFor(tenantId: string) {
  let s = tenantSlots.get(tenantId);
  if (!s) {
    s = new Semaphore(5); // max 5 concurrent heavy ops per tenant
    tenantSlots.set(tenantId, s);
  }
  return s;
}
```

Add eviction for idle tenants to avoid unbounded map growth.

## 29.12 — Queue saturation

A concurrency limit creates a queue. If the queue is unbounded, the limit only moves the failure from
"too many in-flight" to "infinite wait."

```text
arrival rate λ > service rate μ
  → queue grows without bound
  → latency grows without bound
  → eventually timeouts, memory, or OOM
```

### Signs of saturation

| Signal | Meaning |
| ------ | ------- |
| Queue depth trending up | Arrivals exceed service rate |
| Wait time approaching timeout | The queue is too long to drain |
| p99 latency climbing while p50 stable | Queueing, not slower work |
| Timeouts increasing | Requests expire before being served |

### Bounded queues and rejection

```ts
class BoundedPool {
  constructor(private limit: number, private maxQueue: number) {}

  async run<T>(fn: () => Promise<T>): Promise<T> {
    if (this.inFlight >= this.limit && this.queue >= this.maxQueue) {
      throw new OverloadedError("QUEUE_FULL", { retryAfterMs: 1000 });
    }
    // ...enqueue, then execute when a slot frees
  }
}
```

When the queue is full, return `503` (or `429` for rate limits) **immediately** with `Retry-After`.
Rejecting early is kinder than accepting work that will time out.

> ⚠️ **Hazard.** An unbounded queue under overload is a memory leak with extra steps. It also makes
> latency unbounded, which defeats the timeout you carefully set.

## Worked example — Little's Law

Provider allows **50 req/s**. Observed p99 latency **400ms**. Safe concurrency:

```text
concurrency = 50 × 0.4 = 20
```

Set the semaphore to **20**, queue max to **40** (about two seconds of work), and reject beyond that
with `503`. Before this, Acme allowed 200 concurrent calls, the provider rate-limited them, retries
made it worse, and the queue grew to thousands.

## Key data / numbers

- Little's Law: `concurrency ≈ throughput × latency`.
- Per-dependency concurrency: derived from provider limits and p99 latency.
- Per-tenant concurrency: commonly **2–10** for heavy operations.
- Queue bound: roughly **1–2×** the concurrency limit in seconds of work.
- Rejection response: `503`/`429` + `Retry-After`.
- Pool headroom: keep **20–30%** unused for bursts and failover.

## Real-world use case — Acme SaaS

Acme ran all outbound HTTP through one 100-connection pool. A customer's `ExportJob` opened 80
parallel calls to a slow S3-compatible provider, leaving only 20 connections for Stripe, auth, and
email. Checkout began failing with pool timeouts even though Stripe was healthy. Splitting pools
(Stripe 20, storage 30, general 50) and capping each tenant at 5 concurrent export calls isolated the
noisy customer. Checkout errors during the next large export dropped from ~12% to zero.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| One shared pool | Simple, efficient | Noisy-neighbor risk |
| Per-dependency pools | Isolates failures | More config, partial idle |
| Per-tenant limits | Fairness | State per tenant, eviction needed |
| Bounded queue + reject | Predictable latency | Some requests fail fast |
| Unbounded queue | Absorbs bursts | Unbounded latency/memory |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Partition by dependency and tenant | Share one pool for everything |
| Derive limits from Little's Law | Guess a round number |
| Bound the queue | Let it grow without limit |
| Reject with `503` + `Retry-After` | Accept work that will time out |
| Keep pool headroom | Run at 100% utilization |
| Evict idle tenant state | Leak a semaphore per tenant forever |

## Common mistakes

- **Concurrency limit without a queue bound**, moving the problem to memory.
- **Limit above the connection pool**, causing pool timeouts anyway.
- **Per-tenant limits with no eviction**, growing memory unbounded.
- **Rejecting with `500`**, which looks like a bug rather than overload.
- **Ignoring p99 latency** when sizing concurrency.

## Checklist

- [ ] Pools are separated by dependency.
- [ ] Heavy workloads have per-tenant limits.
- [ ] Limits are derived from provider limits and latency.
- [ ] Queues are bounded.
- [ ] Overload returns `503`/`429` + `Retry-After`.
- [ ] Pool headroom is reserved.
- [ ] Idle tenant state is evicted.
- [ ] Queue depth and wait time are monitored.

## Related

- [Admission Control and Combining Mechanisms](./04-admission-control-and-combining-mechanisms.md)
- [Timeouts and Bulkheads for Acme](../03-practical-examples/02-timeouts-and-bulkheads-for-acme.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
- [Chapter 29 Reference](../05-reference/README.md)
