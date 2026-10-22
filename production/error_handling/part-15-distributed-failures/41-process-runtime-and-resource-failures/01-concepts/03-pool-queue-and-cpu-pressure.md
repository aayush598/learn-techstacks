# Pool, Queue, and CPU Pressure (41.7–41.9)

> Part XV · Chapter 41 · Sections 41.7–41.9 · _Estimated reading time: 22 min_
> **Prerequisite:** [Memory, Stack, and Descriptor Exhaustion (41.3–41.6)](./02-memory-stack-and-descriptor-exhaustion.md)

## In one sentence

**Pool exhaustion, queue saturation, and CPU pressure are saturation failures**: the work cannot
be done *now*, so the system must **reject explicitly** (`503`/`429` + `Retry-After`) instead of
**queueing without a bound** — an unbounded wait turns a slowdown into an outage.

## Why this matters in production

Saturation is the failure mode that *looks* like a network problem. A request that waits 30
seconds for a database connection and then times out looks exactly like a slow database, a slow
network, or a slow downstream — and you will spend the incident tuning the wrong thing. The
reality is usually mundane: **a pool of 10 connections and 200 concurrent requests**.

The other thing that makes saturation dangerous is that the *fix* people reach for first — add
more waiting — makes it worse. If requests queue behind a saturated pool with no timeout, the
queue becomes the bottleneck, latency grows without bound, and every waiting request holds
memory, a socket, and possibly a database session. The service stops being slow and starts being
down, with **no error rate change** to alert on.

## Core concept

### 41.7 Pool exhaustion

A **pool** exists because the thing behind it is scarce and expensive: database connections, HTTP
keep-alive sockets, worker threads, upstream API quota. A pool converts "unlimited concurrent
demand" into "bounded concurrency with a waiting room".

```text
  200 concurrent requests  →  pool (max 10)
                             active: 10   idle: 0   waiting: 190
                             190 requests WAIT for a connection (indefinitely, by default)
```

Pool exhaustion has four distinguishable causes, and they need four different fixes:

| Cause | Signature | Fix |
|-------|-----------|-----|
| **Pool too small** | `waiting` grows, `active` pinned at max, queries are fast | size the pool from the *server's* budget, not from the app's core count |
| **Connections held too long** | `active` pinned, each query slow, DB shows long sessions | fix the query; set `statement_timeout`; move reporting off the request path |
| **Connections never released** | `active` grows to max and never returns | the leak is in your code — `finally`/`defer`/context manager |
| **Retry amplification** | `waiting` spikes right after an incident | one owner of retries, and the retry must not hold a connection while waiting |

⚠️ **Hazard.** The most common pool bug is **acquiring with no timeout**: it converts a pool
problem into a request-queue problem, and the queue has no limit either. The correct acquire has
a deadline shorter than the request deadline, and fails with a **`503` that says "busy"**, not a
`500` that says "unknown".

**Sizing is a budget negotiation, not a tuning exercise.** The pool must fit inside what the
server allows:

```text
total connections the database allows
  = max_connections (Postgres default: 100)
  − reserved (superuser_reserved_connections, default: 3)
  − headroom for migrations, monitoring, and admin (keep ~20%)
per-instance pool size = that share ÷ number of instances
```

For Postgres specifically, the per-instance pool must be **small**: `10` connections × 20 pods =
`200` attempted connections against a `max_connections` of `100`. The failure is then *not* a
timeout in your code — it is the database refusing with **`SQLSTATE 53300` too_many_connections**,
a *fatal* connection error, not a queueing condition.

**Bulkheads** (see [Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/01-concepts/03-bulkheads-and-concurrency-limits.md))
make the pool budget explicit: one pool for interactive traffic, one for background jobs, one per
tenant tier, so a reporting query that exhausts the shared pool degrades reporting only.

### 41.8 Queue saturation

A **queue** is a promise that work will happen later. If the arrival rate exceeds the service
rate, the queue grows without bound, and the latency it reports is fiction.

```text
arrival rate λ > service rate μ ⇒ queue grows ⇒ latency grows ⇒ memory grows
                                          └── the failure is a DELAYED outage
```

The three rules for a queue you can survive:

1. **Bound the queue.** An unbounded in-memory queue is a memory leak with extra steps. When it is
   full, **reject** (`429`/`503`) rather than accept work you cannot start.
2. **Measure depth *and* age.** Depth alone is ambiguous: a deep queue of old work is an outage; a
   deep queue of fresh work is a burst. **Age of the oldest item** is the number that pages.
3. **Shed before you collapse.** Shedding load deliberately (rejecting cheap requests, degrading
   optional features) keeps the core working. Shedding *reactively* — when everything is slow —
   looks identical to the outage it was supposed to prevent.

Backpressure only works if it reaches the producer: the producer must learn that it is too fast,
via a `429`/`503` with `Retry-After`, or a queue-side admission limit.

⚠️ **Hazard.** **Queueing an error is a way of hiding it.** A retry that is enqueued instead of
surfaced keeps the failure off the error-rate dashboard while the work is retried forever. If a
job is retried, it must have an attempt count, a backoff, and a terminal state (DLQ) — and the
DLQ depth must be a metric.

### 41.9 CPU and memory pressure

CPU pressure is the *scarcest* resource in a container, because it is the one the scheduler
**throttles** rather than kills.

| Signal | Meaning | Where to look |
|--------|---------|---------------|
| **Event-loop lag** (Node) | the single-threaded loop is busy; everything queues behind it | `eventloop.lag` / `monitorEventLoopDelay` |
| **Container CPU throttling** | the cgroup exhausted its quota in a period and the process was **paused** | `cpu.stat` → `nr_throttled`, `throttled_usec` |
| **GC pressure** | allocation outpaces collection; CPU is spent collecting | heap `used` vs `total`, GC pause time |
| **Run-queue length** | more runnable threads than cores | `runqueue` metric |

The container case is the one that surprises people: a container with a CPU **limit** does not get
"slower CPU", it gets **stopped for the rest of the period**. A CPU limit of `1` with a CFS period
of **100 ms** means the process gets **100 ms of CPU per 100 ms period**, and excess work is
**throttled for the remainder** — a latency spike that looks like an I/O stall in a service doing
nothing but arithmetic.

Memory pressure has a quieter cousin: the **listener leak**. Every `emitter.on(...)` without a
matching `off` retains its closure and its captured scope. Node warns at the 11th listener on one
emitter with **`MaxListenersExceededWarning`** (default `maxListeners` = **10**) — a **leak
detector**, and the leak it reports grows with traffic.

```text
per-request listener registration (a classic bug)
  request 1   → emitter.on('data', cb₁)      → 1 listener
  request 11  → MaxListenersExceededWarning  ← the runtime is telling you the truth
  request 500 → 500 listeners, 500 closures retained → RSS grows forever
```

## How it works (mechanics)

### The saturation cascade (the shape of every saturation incident)

```text
1. something slows: a query, a GC pause, a downstream slowdown
2. connections/workers stay busy longer → waiters appear (pool waiting ↑, queue depth ↑)
3. memory grows: each waiter holds a request, a socket, a buffer
4. the health check times out (a victim of the same saturation) → the pod is killed
5. the remaining pods get its traffic → they saturate too
```

Step 4 is the one teams design badly. A **liveness probe that depends on the saturated
dependency** converts partial degradation into a **restart storm**. Liveness should answer "is
this process wedged?", not "is the database fast?".

### Bounding a pool acquire

```ts
const ACQUIRE_TIMEOUT_MS = 1_000;   // < request timeout, > typical query time

export async function withDb<T>(fn: (c: PoolClient) => Promise<T>): Promise<T> {
  const client = await pool.connect({ timeout: ACQUIRE_TIMEOUT_MS });
  try {
    return await fn(client);
  } finally {
    client.release();                 // ← always release, even on throw
  }
}
```

With a timeout, the acquire fails fast and the request can be answered with a **`503` + a stable
code + `Retry-After`**:

```ts
try {
  return await withDb((c) => c.query("SELECT ..."));
} catch (err) {
  if (isPoolTimeout(err)) {
    metrics.increment("db_pool_timeout");
    throw new DomainError("DB_POOL_EXHAUSTED", { http: 503, retryable: true, cause: err });
  }
  throw err;
}
```

That converts an invisible hang into a **visible, alertable** failure.

### Admission control for a queue

```text
if queue.depth > HIGH_WATERMARK:  reject 429/503 (Retry-After: N)
if queue.depth > LOW_WATERMARK:   stop accepting NEW work, keep draining
if oldest_item_age > MAX_AGE:     page — this is an incident, not a backlog
```

## Worked example

```python
# ❌ No acquire timeout: a saturated pool becomes an unbounded request queue.
def get_tenant(conn_info, tenant_id):
    conn = psycopg2.connect(**conn_info)      # ← new connection per call, no bound
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM activity_feed WHERE tenant_id = %s", (tenant_id,))
        return cur.fetchall()
```

```text
the activity-feed query loses its index → each call takes 30 s
  → 200 concurrent requests → 200 Postgres sessions → max_connections = 100
  → SQLSTATE 53300 too_many_connections; the pool (10) is fully held by the slow queries
  → 190 requests wait on acquire, with no timeout
  → the pod's health check times out → the pod is killed
  → its traffic lands on the other 19 pods → they slow down → more kills
  → total outage, and the only log line is "connection timeout"
```

The fixed version bounds every layer:

```python
POOL_SIZE = 5            # 20 pods × 5 = 100 sessions; leave 20% headroom for the DB
ACQUIRE_TIMEOUT = 1.0    # seconds; fail fast with 503 instead of queueing forever

def get_tenant(pool, tenant_id):
    try:
        with pool.connection(timeout=ACQUIRE_TIMEOUT) as conn:
            conn.cursor().execute("SET statement_timeout = '5s'")
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, kind, created_at FROM activity_feed "
                    "WHERE tenant_id = %s ORDER BY created_at DESC LIMIT 200", (tenant_id,))
                return cur.fetchall()
    except PoolTimeout:
        raise ServiceBusy("DB_POOL_EXHAUSTED", http=503, retry_after=2)
```

Notice the three separate bounds: **pool size** (sessions), **acquire timeout** (waiting), and
**`statement_timeout`** (how long one query may hold a session).
## Key data / numbers

- **Postgres** `max_connections` default **100**, `superuser_reserved_connections` default **3**;
  `SQLSTATE 53300` `too_many_connections`, `53200` `out_of_memory`. MySQL: `1040` too many
  connections. Redis `maxclients` default **10000**.
- **Pool acquire timeout**: pick it **below the request deadline and above the p99 query time**;
  a common working range is **0.5–2 s**, and the HTTP layer's timeout must be larger.
- **Postgres `statement_timeout`**: set it per role or per pool session (commonly **5–30 s**);
  a query with no timeout can hold a session until the client gives up.
- **Node** `EventEmitter` default `maxListeners` = **10** → the 11th listener emits
  **`MaxListenersExceededWarning`**. Raise it deliberately with `emitter.setMaxListeners(n)` —
  never to silence a leak.
- **cgroup CPU throttling**: CFS period default **100000 µs (100 ms)**; a container with a CPU limit
  is *paused* for the unused part of each period. Watch `cpu.stat` → `nr_throttled`.
- **Container memory limits**: cgroups v2 `memory.max`; Kubernetes `resources.limits.memory`;
  the OOM kill exits **137**.
- **HTTP** `429 Too Many Requests` and `503 Service Unavailable` are the two correct answers to
  shedding; both should carry **`Retry-After`**.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` shared one Postgres pool of 10 with the reporting queries behind the
admin dashboard. A customer's analytics page ran a query that scanned the whole `events` table
(no index on `(tenant_id, created_at)`), and each call held a connection for ~25 seconds. The
pool's 10 connections were consumed within a minute, and the ingest requests — which had **no
acquire timeout** — queued indefinitely. The service's `/healthz` endpoint queried the same
database, so it timed out and the orchestrator killed the pod. The restarted pod received a
burst of redelivered webhooks and the cycle repeated: **a 20-minute total ingest outage**.

The fix was four bounds and one separation:

- pool acquire timeout **1 s** → `503 DB_POOL_EXHAUSTED` with `Retry-After: 2`;
- the missing index (additive, online) → the query went from 25 s to 12 ms;
- `statement_timeout = 5s` on the ingest pool role;
- a **separate pool for reporting** (bulkhead), so an admin page can never eat ingest capacity;
- the liveness probe changed to a **process-local** check (event loop responsive + heartbeat age).

Post-fix, the same admin page saturates only the reporting pool; ingest p99 stayed at 90 ms, and
the new `db_pool_timeout` metric caught a second slow query **before** it reached users.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Bounded pool + acquire timeout** | fails fast, visible, client-actionable | requires client retry handling | default for every pool |
| **Bounded queue + rejection** | protects the core, honest 429/503 | rejects work that could have waited | default for job intake |
| **Unbounded wait / unbounded queue** | no errors, no rejections | converts saturation into an outage | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set an acquire timeout on every pool | Wait for a connection forever |
| Size the pool from the server's connection budget | Size the pool from the app's core count |
| Use a separate pool per workload class (bulkhead) | Share one pool across tenants and workloads |
| Set `statement_timeout` on every session | Let one query hold a session indefinitely |
| Bound queue depth and reject past the watermark | Accept work you cannot start |
| Alert on queue **age**, not only depth | Alert only on depth |
| Probe liveness process-locally | Probe liveness through a saturated dependency |

## Common mistakes

- **No acquire timeout** — the single most common cause of "the database is down" tickets that
  are really "the pool is full".
- **A liveness probe that queries the database** — the probe becomes part of the saturation and
  the orchestrator kills healthy pods.
- **Sizing pools per instance without multiplying by instance count** — 20 pods × 10 = 200
  sessions against Postgres's 100.
- **Sharing a pool between interactive and background work**, or **unbounded retries that
  re-acquire a connection** — a nightly report can starve checkout, and the retry storm competes
  with the original traffic for the same 10 connections.

## Checklist

- [ ] Every pool has an explicit size, an acquire timeout, and a release path on all exits.
- [ ] Pool size × instance count fits inside the server's connection budget, with headroom.
- [ ] `statement_timeout` is set for every session/pool role.
- [ ] Separate pools (bulkheads) for interactive, background, and per-tenant-tier work.
- [ ] Every queue has a bounded depth, a rejection response (`429`/`503` + `Retry-After`), and an
      age-based alert.
- [ ] `eventloop.lag`, pool `waiting`, queue depth/age, RSS, and CPU throttling are monitored.
- [ ] Liveness probes check the process, not its dependencies.
- [ ] `MaxListenersExceededWarning` is treated as a defect, not noise.

## Related

- [Initialization, Startup, and Shutdown (41.10–41.18)](./04-initialization-startup-and-shutdown.md)
- [Python and Go: OOM and Resource-Limit Handling](../03-practical-examples/02-python-and-go-resource-limit-handling.md)
- [Bulkheads and Concurrency Limits](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/01-concepts/03-bulkheads-and-concurrency-limits.md)
- [Admission Control and Combining Mechanisms](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/01-concepts/04-admission-control-and-combining-mechanisms.md)
- [Connection and Pool Errors](../../../part-09-database-and-transactions/22-database-error-classification/01-concepts/01-connection-and-pool-errors.md)
