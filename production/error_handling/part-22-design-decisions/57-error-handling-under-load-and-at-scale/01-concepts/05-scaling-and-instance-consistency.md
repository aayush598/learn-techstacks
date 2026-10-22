# Scaling Horizontally and Staying Consistent Across Instances

> Part XXII · Chapter 57 · Sections 57.16, 57.17, 57.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)

## In one sentence

Horizontal scaling multiplies instances but not **isolation**, so the error path must be
**stateless and policy-identical** on every instance — because a shared mutable counter in
the error path becomes a contention point exactly when the system is failing.

## Why this matters in production

A single-instance system can hide several design errors that only appear when you scale out:

- A **module-level circuit breaker** is per-process. With 10 instances, a dependency that is
  down for one instance (because it failed through that instance's circuit breaker) is still
  being called by the other 9. The breaker stops working exactly when you need it.
- A **per-instance retry budget** means the effective budget is `N × 10%`, so a storm's
  amplification grows with your instance count — the opposite of what scaling should do.
- A **shared counter with a mutex** (in Redis, in the database) serializes every error event
  through one round trip. At 10,000 errors/second, the counter becomes the bottleneck and
  adds latency to the error path.
- A **local in-memory cache of failures** means instance A retries a dependency that
  instance B has already marked dead — so the fleet keeps hammering it.

## Core concept

### 57.16 — What horizontal scaling actually multiplies

```text
  ┌──────────── instance 1 ────────────┐   ┌──────────── instance 2 ────────────┐
  │ breaker(stripe)  [open]            │   │ breaker(stripe)  [closed]          │
  │ retryBudget     10%                │   │ retryBudget     10%                │
  │ tenantLimit(t1) 10                 │   │ tenantLimit(t1) 10                │
  │ pool            20                 │   │ pool            20                 │
  └────────────────────────────────────┘   └────────────────────────────────────┘
                    ↑                              ↑
            each is INDEPENDENT unless you make it shared
```

Scaling multiplies **capacity** (more requests served) and **failure modes** (more places to
be inconsistent). It does not multiply **isolation**: if all instances share one Postgres
pool, one tenant can still consume everyone's connections.

| Component | Per-instance or shared? | Consequence |
| --------- | ---------------------- | ----------- |
| Connection pool | Per instance | Total DB connections = `instances × pool`; must fit `max_connections` |
| Circuit breaker | **Shared state needed** for correctness | Per-instance breakers are 1/N effective |
| Retry budget | **Shared** | Per-instance budgets scale the storm with the fleet |
| Tenant concurrency limit | **Shared** (or accept N× slack) | Per-instance limits let a tenant use N× its share |
| Rate limiter | Shared (Redis) | Per-instance limiters are N× the intended limit |
| Error counters | Per-instance, aggregated centrally | A shared counter is a bottleneck |
| Queue | Shared | Otherwise work is processed by only one instance |
| Config / policy | Shared source | Divergent policy = divergent behavior |

The arithmetic that catches teams: **10 instances × a 20-connection pool = 200 database
connections**. If Postgres `max_connections` is 100, the fleet cannot even start. Acme's
rule: `instances × pool_per_instance ≤ 40% of max_connections`, leaving room for migrations,
admin sessions, and the read replica.

### 57.17 — Consistent policy across instances

Three things must be identical on every instance:

1. **The code** — trivially true if you deploy the same artifact. (Blue/green and canary
   deployments break this temporarily; see below.)
2. **The configuration** — retry counts, timeouts, breaker thresholds, shed order. If
   instance A has `attempts: 3` and instance B has `attempts: 1`, behavior is
   nondeterministic and the fleet's error rate becomes a distribution, not a number.
3. **The shared state** — breaker state, retry budget, rate-limit counters.

The practical mechanisms:

| Mechanism | Use for | Trade-off |
| --------- | ------- | --------- |
| Ship config in the artifact | Immutable policy | Requires a deploy to change |
| Read config from a config service at boot | Tunable policy | Needs a cached copy + a fallback |
| Feature flags (evaluated per request) | Gradual rollout | Flag evaluation cost per request |
| Shared breaker state (Redis) | Fleet-wide breakers | A Redis round trip per call |
| Local breaker + shared "kill switch" | Best of both | Two mechanisms to reason about |

> ⚠️ **Hazard.** **A shared breaker in Redis adds a network round trip to every dependency
> call.** When Redis is slow, the breaker check is slow, and the error path — the part that
> must be fastest — becomes the slowest. The standard resolution: a **local breaker with a
> shared kill switch**. Each instance breaks locally and instantly; the kill switch (a single
> flag, cached for a few seconds) propagates "this dependency is down, stop calling it"
> fleet-wide.

### 57.18 — Avoiding shared mutable state

The rule for the error path:

> **The error path must be stateless.** It may *read* shared state; it must not *write* to it
> synchronously.

| Write in the error path | Why it is dangerous | Instead |
| ----------------------- | ------------------- | ------- |
| `INCR acme:errors:{code}` on every error | A round trip per error; contention | Local counter, flushed periodically |
| `SET acme:breaker:{dep} open` on failure | The breaker becomes a network dependency | Local breaker + shared kill switch |
| Publishing a "failure" event | A broker round trip per error | Emit locally, aggregate upstream |
| Writing a "recent failures" list | Lock contention exactly during an incident | Local ring buffer |
| Distributed lock around the error path | Serializes all failures | Never lock in the error path |

The deeper reason: **the error path is the path that runs when the system is least healthy**.
Any shared dependency it touches is a dependency that may itself be the thing that is failing.
An error path that needs Redis to record an error will fail to record the error when Redis
is down — and it will do so *slowly*, adding latency to every failing request.

```ts
// ❌ A network round trip on every error, to a store that may be down.
catch (err) {
  await redis.incr(`errors:${code}`);
  throw err;
}

// ✅ Local, non-blocking, and eventually aggregated.
catch (err) {
  localErrorCounter.increment(code);   // in-process, microseconds
  throw err;
}
// A background task flushes local counters to the metrics backend every 10 s.
```

### Blue/green and canary: policy must be versioned with the code

During a canary, two policy versions coexist. If a canary instance has a different retry
count, it behaves differently — and its errors pollute the comparison.

Rules:

1. **Error-handling policy travels with the artifact.** Config that changes retry counts or
   breaker thresholds is versioned and deployed, not fetched at runtime during a rollout.
2. **Only the safe direction may differ.** A canary may have *fewer* retries (safer) but not
   more.
3. **Compare error rates by policy version**, not just by instance, when a rollout is in
   flight.
4. **The kill switch is the one thing that must be runtime-changeable** — precisely because
   it is the mechanism for stopping a bad rollout.

## How it works (mechanics)

### A shared kill switch with local breakers

```ts
export class KillSwitch {
  private state: { open: boolean; fetchedAt: number } | null = null;
  private static readonly TTL_MS = 5_000;

  constructor(private readonly source: ConfigSource) {}

  isOpen(dependency: string): boolean {
    const now = Date.now();
    if (!this.state || now - this.state.fetchedAt > KillSwitch.TTL_MS) {
      // Read synchronously from an in-process cache refreshed by a background task.
      // Never await a network call on the request path.
      this.state = { open: this.source.cached().killSwitch[dependency] ?? false, fetchedAt: now };
    }
    return this.state.open;
  }
}

// In the adapter:
if (killSwitch.isOpen("stripe")) {
  throw new DependencyDisabledError({ dependency: "stripe" });   // instant, no network
}
```

### Local breaker + shared counter, aggregated upstream

```ts
export class ErrorCounter {
  private readonly counts = new Map<string, number>();
  private lastFlush = Date.now();

  increment(code: string): void {
    this.counts.set(code, (this.counts.get(code) ?? 0) + 1);
  }

  // Called by a background task every 10 s — never on the request path.
  flush(metrics: MetricsClient): void {
    const now = Date.now();
    if (now - this.lastFlush < 10_000) return;
    for (const [code, count] of this.counts) {
      metrics.increment("error.count", count, { code });
    }
    this.counts.clear();
    this.lastFlush = now;
  }
}
```

### Verifying fleet-wide consistency

A test that catches the classic divergence:

```ts
describe("error policy consistency across instances", () => {
  it("uses identical retry and timeout policy on every instance", async () => {
    const instances = await fleet.instancePolicies();
    const distinct = new Set(instances.map((p) => JSON.stringify(p)));
    expect(distinct.size).toBe(1);
  });

  it("computes a fleet-wide retry budget, not a per-instance one", async () => {
    const budget = await retryBudget.sharedRatio();       // e.g. 0.10 across the fleet
    expect(budget).toBeLessThanOrEqual(0.10);
  });
});
```

The second test is the important one: a per-instance budget means the fleet's budget grows
with the instance count, which means the storm grows with the fleet.

## Worked example — `Acme SaaS` scaling from 4 to 24 instances

Acme grew from 4 to 24 application instances over two quarters. Three scale-induced defects
appeared.

### Defect 1 — the database connection wall

At 24 instances × 20 connections = 480 connections against a Postgres with
`max_connections = 500`. Acme hit "too many clients" during a rolling restart, because old
and new instances overlapped.

Fix: `pool = 12` per instance, `24 × 12 = 288` = 58% of `max_connections`; plus
`connectionTimeoutMillis = 250` so excess callers fail fast instead of queueing. Acme also
moved the analytics queries to the read replica, which removed 90 connections' worth of
pressure.

### Defect 2 — the breaker that only worked on one instance

A Stripe incident: 4 of 24 instances opened their breaker and stopped calling Stripe; the
other 20 kept calling. The dependency stayed saturated for 11 minutes after Stripe's own
recovery.

Fix: a **local breaker plus a shared kill switch**. When a breaker opens locally, the
instance sets a shared flag (`killSwitch:stripe=open`) with a 5-second TTL; every instance
polls that flag in the background and opens locally within 5 s. Result: all 24 instances
stopped within 5 seconds instead of 4 out of 24 stopping immediately.

### Defect 3 — the shared counter that became the bottleneck

The error counter did `await redis.incr(...)` in the catch block. During a database
incident, Redis got slow (it shares the same host as Postgres on two instances), and every
failing request added a Redis round trip *before* responding. The error path's latency
became Redis's latency.

Fix: local counters, flushed every 10 s by a background task. The error path now has **zero
network calls**.

### What Acme changed, and the result

| Change | Before | After |
| ------ | ------ | ----- |
| Pool per instance | 20 | 12 (288 fleet-wide) |
| `connectionTimeoutMillis` | 0 (wait forever) | 250 ms |
| Breaker scope | per instance (4/24 effective) | local + shared kill switch (24/24 in ≤ 5 s) |
| Retry budget | per instance (10% × N) | fleet-wide 10% |
| Error counter | Redis `INCR` per error | local, flushed every 10 s |
| Error-path network calls | 1 per error | 0 |

Measured during a simulated Stripe incident at 24 instances: the fleet stopped calling
Stripe within 5 seconds (was: 11 minutes of partial protection), the retry ratio stayed at
0.06 (was: 0.38), and the error path's p99 latency was 3 ms (was: 340 ms, dominated by the
Redis round trip).

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Fleet-wide DB connections | ≤ 40% of `max_connections` | Leave room for migrations and admin |
| Pool per instance | 12–20 | `fleet × pool ≤ 0.4 × max_connections` |
| `connectionTimeoutMillis` | 250 ms | Never 0 |
| Breaker state scope | Local + shared kill switch | Kill switch TTL 5 s |
| Kill switch propagation target | ≤ 5 s | Must be faster than the recovery it triggers |
| Retry budget scope | Fleet-wide | Per-instance budgets scale the storm |
| Tenant limit scope | Shared, or accept N× slack | Document which |
| Error counter scope | Per instance, flushed | Never write synchronously to a shared store |
| Error-path synchronous network calls | **0** | Reads of cached config are fine |
| Config consistency | Same artifact, same policy | Config-as-code, versioned |
| Local counter flush interval | 10 s | Acceptable staleness for metrics |
| Blue/green policy difference | Only "fewer retries" | More retries in a canary is unsafe |
| Rate limiter scope | Shared (Redis) | Per-instance = N× the intended limit |
| Min instances for a fleet-wide budget to matter | 2 | Never design per-instance at scale |

## Real-world use case — `AgentRun` (Acme SaaS) at 30 instances

`AgentRun` is stateful in a way that made scaling awkward: the original implementation kept
a **per-process map of in-flight runs** used to prevent duplicate tool writes. With 30
instances, a duplicate could land on another instance.

The bug: a run retried by the client was dispatched to instance B, which did not know
instance A was already running it, so the tool write executed twice — a T3 duplication.

The fix had two parts:

1. **Move the guard to shared, idempotent state.** The tool write is keyed by
   `runId:toolCallId` in the database with a unique constraint. Now the guard is *the write
   itself*, not an in-memory map. Any instance, any retry, any duplicate is collapsed by the
   database.
2. **Keep the error path stateless.** The run's error is recorded in the run's own row
   (`runs.last_error`), written as part of the same transaction — not in a shared in-memory
   map.

The general lesson: **when you need cross-instance coordination in the error path, prefer an
idempotency constraint in the store over coordination in memory.** Memory does not scale
horizontally; a unique constraint does.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Per-instance breakers | No network cost | Only 1/N effective | Small fleets, or with a kill switch |
| Shared breaker state | Fleet-wide correctness | A network round trip per call | Critical dependencies only |
| Local breaker + kill switch | Fast locally, correct fleet-wide | Two mechanisms; a short window of inconsistency | **Default** |
| Per-instance retry budget | Simple | Budget scales with the fleet | Never at scale |
| Fleet-wide retry budget | Correct amplification | Needs shared state | **Default at scale** |
| Shared counter (synchronous) | Exact counts | Bottleneck; slow on failure | Never |
| Local counter + flush | Fast, non-blocking | Up to 10 s of staleness | **Default** |
| Idempotency constraint | Scales, survives restarts | Requires a unique index | Any cross-instance coordination |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the error path free of synchronous network calls | `await redis.incr()` in a catch block |
| Use a local breaker plus a shared kill switch | Rely on a per-instance breaker at 20+ instances |
| Budget retries fleet-wide | Give each instance its own retry budget |
| Coordinate with idempotency constraints | Coordinate with in-memory maps across instances |
| Ship error policy in the artifact | Fetch changing retry counts from a service mid-rollout |
| Bound fleet-wide DB connections | Multiply the pool by the instance count blindly |
| Allow a canary to have *fewer* retries | Give a canary more retries than production |

## Common mistakes

- **Per-instance state that was correct at 2 instances.** A "just a counter" becomes a
  fleet-wide rate limiter as soon as you scale.
- **A shared counter that becomes the bottleneck.** The error path should never wait on
  anything.
- **Rolling restarts that double the fleet's connections.** Overlapping old and new
  instances can exceed `max_connections` even when the steady state is fine.
- **Config drift between instances.** A `Retry-After` cap that differs by instance produces
  nondeterministic behavior that looks like a partial outage.
- **Blue/green with a different retry policy.** The canary's extra retries become extra load
  on the very dependency being tested.

## Checklist

- [ ] `instances × pool_per_instance ≤ 40% of max_connections`.
- [ ] Every pool has a bounded `connectionTimeoutMillis`.
- [ ] Breakers are local, with a shared kill switch (TTL ≤ 5 s) for fleet-wide propagation.
- [ ] The retry budget is fleet-wide, and the fleet ratio is monitored.
- [ ] Tenant concurrency limits are shared, or the N× slack is documented.
- [ ] The error path performs **zero** synchronous writes to shared stores.
- [ ] Cross-instance coordination uses idempotency constraints, not in-memory state.
- [ ] Error-handling policy ships with the artifact; only the kill switch is runtime-mutable.
- [ ] A consistency test asserts identical policy across instances.

## Related

- [Failure Amplification and Error Storms](./01-failure-amplification-and-error-storms.md)
- [Isolation: Tenants, Features, and Dependencies](./02-isolation-tenants-features-dependencies.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 10 — Centralized and Distributed Error Handling](../../../part-04-architecture/10-centralized-and-distributed-error-handling/README.md)
