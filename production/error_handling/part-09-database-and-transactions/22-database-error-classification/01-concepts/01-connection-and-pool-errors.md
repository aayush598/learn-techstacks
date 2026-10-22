# Connection Establishment and Pool Exhaustion (22.1, 22.2)

> Part IX · Chapter 22 · Sections 22.1, 22.2 · _Estimated reading time: 18 min_
> **Prerequisite:** [Error Categories in Detail (5.13 Database)](../../../part-02-error-taxonomy/05-error-categories-in-detail/01-concepts/02-limits-concurrency-and-data.md)

## In one sentence

Connection errors (**class `08`**) mean *you could not talk to the database*, while pool
exhaustion (**`53300`** or a client-side pool timeout) means *you never got a chance to try* —
and **mistaking one for the other hides a capacity problem behind a network story**.

## Why this matters in production

During a launch week, Acme's API started returning `500`s. The logs said "connection refused",
so the team checked the network for an hour. The real cause: **`database/sql`'s default
`SetMaxOpenConns(0)` is unlimited**, the primary's `max_connections` is **100** by default, and
one chatty endpoint opened connections as fast as the pool could hand them out. The database
began rejecting the 101st connection with **`53300 too_many_connections`**. Treating `53300`
like an infrastructure outage delayed the fix (bound the pool) and caused a retry loop that made
it worse.

## Core concept

Two different layers can fail before a row is ever read:

```text
App ──▶ [client pool] ──▶ [TCP + auth] ──▶ [server: max_connections] ──▶ query
         │                     │                       │
         │ pool timeout        │ 08001 / 08006         │ 53300
         │ (client-side,       │ (network/auth/        │ (server-side,
         │  no SQLSTATE)       │  TLS, wrong host)      │ real SQLSTATE)
         └─────────────────────┴───────────────────────┘
              "no connection"          "connection refused"
```

| Failure | Where | Signal | Root cause class |
| ------- | ----- | ------ | ---------------- |
| DNS / wrong host / TLS | client | `08001`, driver error, `ECONNREFUSED` | config / network |
| Auth failure | server | `28000`, `28P01`; MySQL `1045` | config / credentials |
| Server unreachable | transport | `08006`, `ECONNRESET`, `2013` (MySQL) | network / failover |
| Server at capacity | server | **`53300`**, MySQL **`1040`** | capacity |
| Pool at capacity | client pool | client-side timeout, **no SQLSTATE** | your configuration |
| Connection dropped mid-use | transport | `08006`, `57P01`, MySQL `2006` | restart / failover / idle kill |

> ⚠️ **Hazard.** A pool timeout is *not* a database error. It has no `SQLSTATE` because no
> server ever saw your query. Alerting on it as "database down" trains on-call to ignore the
> real signal.

## How it works (mechanics)

### Connection establishment (22.1)

1. Client resolves host, opens TCP, negotiates TLS.
2. Client sends `StartupMessage` (Postgres) or handshake (MySQL) with database, user, password.
3. Server authenticates (`28000`/`28P01` on failure) and checks `max_connections` (`53300`).
4. On success the backend is assigned a slot; on any failure the client must classify:
   **config (permanent)** vs **capacity/network (transient)**.

Postgres SQLSTATEs you will actually see:

| SQLSTATE | Meaning | Retry? |
| -------- | ------- | ------ |
| `08001` | `sqlclient_unable_to_establish_sqlconnection` | yes, unless config |
| `08006` | `connection_failure` | **yes, backoff** |
| `08003` | `connection_does_not_exist` | **yes** |
| `53300` | `too_many_connections` | **yes, with backoff + reduce load** |
| `57P03` | `cannot_connect_now` (shutting down/restarting) | **yes** |
| `28P01` | `invalid_password` | **no** — fix config |

### Pool exhaustion (22.2)

A pool sits *in front of* the server. When it is saturated, callers wait, then fail:

```ts
// node-pg: the pool hands out at most `max` connections; the rest queue.
const pool = new Pool({ max: 10, connectionTimeoutMillis: 2_000 });
// After 2s with no free connection: "TimeoutError: resource timed out"
// That error has no SQLSTATE — it is YOUR policy failing, not Postgres.
```

Common defaults that surprise teams:

| Client | Relevant default | Consequence |
| ------ | ---------------- | ----------- |
| Go `database/sql` | `SetMaxOpenConns(0)` = **unlimited** | app DoS-es the server's `53300` |
| node-pg `Pool` | `max` = **10**, `connectionTimeoutMillis` = **0** (wait forever) | request threads pile up |
| SQLAlchemy | `pool_size=5`, `max_overflow=10`, `pool_timeout=30` | 30s waits, then `TimeoutError` |
| HikariCP (JVM) | `maximumPoolSize=10`, connection timeout **30s** | bounded, fails loudly |
| PgBouncer | `default_pool_size=20` | server sees few connections; app still times out |

**Pool exhaustion and `53300` are different alerts.** The first says "size your client pools";
the second says "the server has no slots left for anyone" — often caused by *another* service
or a connection leak (`pgbouncer` stats or `pg_stat_activity` settle it).

## Worked example

```python
# psycopg2 — distinguishing the two before translating anything
import psycopg2
from psycopg2 import OperationalError

def classify_connect_failure(exc: BaseException) -> str:
    if isinstance(exc, OperationalError):
        state = getattr(exc, "pgcode", None)
        if state == "53300":
            return "DB_AT_CAPACITY"      # transient, back off, shrink pools
        if state in ("08006", "08001", "08003"):
            return "DB_UNREACHABLE"      # transient, back off
        return "DB_CONNECT_FAILED"       # unknown: retry once, then page
    if "pool" in str(exc).lower():       # SQLAlchemy TimeoutError, no SQLSTATE
        return "POOL_EXHAUSTED"          # transient, YOUR config, don't page DB on-call
    return "DB_CONNECT_FAILED"
```

```text
Result under a connection storm:
  pool timeout        → POOL_EXHAUSTED   → 503, metric "pool.wait_timeout", no page
  53300 from server   → DB_AT_CAPACITY   → 503 + Retry-After, page if sustained
  08006 during failover → DB_UNREACHABLE → 503, retry automatically
  28P01               → CONFIG error     → 500, page immediately (bad deploy)
```

## Key data / numbers

- Postgres `max_connections` default: **100**. Practical ceiling on one primary is often
  **hundreds**, not thousands — prefer **PgBouncer/pgbouncer-style pooling** plus small app pools.
- `53300 too_many_connections` — server is full; `57P03 cannot_connect_now` — server is
  shutting down; both **transient**.
- MySQL equivalents: **`1040` Too many connections**, **`1045` Access denied**, **`2006` MySQL
  server has gone away**, **`2013` Lost connection during query**.
- Pool defaults: Go unlimited (`0`), node-pg `max=10`, SQLAlchemy `5+10`, HikariCP `10`.
- Recommended client behavior: **connect timeout 2–5 s**, `connectionTimeoutMillis`/`pool_timeout`
  never `0` in a request path, and a **pool metric that alerts before `53300` does**.

## Real-world use case — Acme SaaS

Acme's `Checkout` flow ran five queries per request over one shared pool of 10. A bulk import
spiked to 200 concurrent requests; the pool saturated, requests waited, and when connections
*did* free up, the burst hit Postgres and produced `53300`. Retries re-entered the same pool
and amplified the queue. The fix had three parts: **separate pools per workload** (bulkhead),
`max=25` with `connectionTimeoutMillis=2000` for the API and a `max=5` pool for imports, and a
`53300`/pool-timeout classifier that returns `503` + `Retry-After` **without retrying inside
the request**. Checkout's p99 stopped cliffing during imports.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| One shared pool | simple | noisy neighbor, one workload starves all | tiny apps, single workload |
| Pool per workload/tenant class | blast radius bounded | more connections total | any multi-workload service |
| PgBouncer in front | server sees few conns | **transaction pooling breaks session state** (prepared statements, `LISTEN`, session GUCs) | most Postgres services |
| Fail fast (short pool timeout) | protects latency budget | surfaces as `503` under load | request paths with deadlines |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set an explicit max open conns per pool (never Go's default `0`) | Let every request open a connection |
| Separate `POOL_EXHAUSTED` from `DB_UNREACHABLE` in code and alerts | Log both as "connection error" |
| Back off on `53300` and shed load | Retry `53300` in a tight loop |
| Treat `28P01`/`1045` as config, page on deploy | Retry a bad password |
| Alert on pool saturation *before* the server says `53300` | Wait for user-visible `503`s |

## Common mistakes

- **Counting pool timeouts as database outages** — no server was involved; fix the pool.
- **Unlimited Go pools** — the app, not the DB, is the bottleneck; set `SetMaxOpenConns`.
- **Retrying connection storms immediately** — every retry competes for the same slots;
  exponential backoff with jitter is mandatory.
- **Sharing one pool between the API and background jobs** — `ExportJob` will starve `Checkout`.

## Checklist

- [ ] Every pool has an explicit max size and a non-zero acquire/connect timeout.
- [ ] `POOL_EXHAUSTED`, `DB_AT_CAPACITY`, `DB_UNREACHABLE`, and `CONFIG` are four distinct codes.
- [ ] Connection errors are classified before any retry decision runs.
- [ ] `28000`/`28P01`/`1045` alert immediately and are never retried.
- [ ] Pool wait time is a metric with its own threshold.

## Related

- [Conflicts, Locks, and Timeouts (22.9–22.13)](./03-conflicts-locks-and-timeouts.md)
- [Failover, Replicas, and Unavailability (22.14–22.16)](./04-failover-replicas-and-unavailability.md)
- [SQLSTATE Classification Table](../02-deep-dive/01-sqlstate-classification-table.md)
- [Chapter 22 Reference](../05-reference/README.md)
