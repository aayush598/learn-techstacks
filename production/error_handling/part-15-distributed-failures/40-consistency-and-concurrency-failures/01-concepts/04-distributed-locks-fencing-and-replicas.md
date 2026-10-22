# Distributed Locks, Fencing, and Replica Consistency (40.10–40.12)

> Part XV · Chapter 40 · Sections 40.10–40.12 · _Estimated reading time: 24 min_
> **Prerequisite:** [Lock Contention, Deadlocks, and Concurrent Duplicate Requests (40.4–40.7)](./02-lock-contention-deadlocks-and-duplicate-requests.md)

## In one sentence

A **distributed lock is a lease, not a lock** — it expires whether or not you are alive — so a
correct design pairs it with a **fencing token checked by the storage layer**, and treats
**replica reads as possibly stale** for exactly as long as the replication lag.

## Why this matters in production

A worker acquires the `ExportJob` lock, pauses for 2 s during a GC or a network blip, its lease
expires, a second worker takes over — and now **both** are writing to the same S3 object while the
first believes it holds the lock. This is the failure mode that distributed locks introduce
*instead of* the race they were supposed to remove. Nearly every "our lock library is buggy" story
is actually "we had a lease without fencing" or "we forgot that a lease is only a promise about
*the future*, not about the past."

## Core concept

### 40.10 Distributed locks and lease expiry

A lease is an assertion with a deadline:

```text
acquire(owner, ttl=10s) ──▶ holder works ──▶ release()
                                │
                     lease expires (holder paused/partitioned)
                                │
                     another holder acquires  ──▶ TWO holders exist in wall-clock overlap
```

| Property | Implication |
|----------|-------------|
| **Time-bounded** | correctness cannot depend on the holder being alive to release |
| **Not re-entrant by default** | re-acquiring from the same process can deadlock or reset unexpectedly |
| **Monotonic clock matters** | wall-clock jumps (NTP) shorten or lengthen leases unpredictably |
| **Expiry is silent** | the holder is *not* notified reliably — a partition looks like slowness |
| **Overlap is possible** | old holder + new holder can both be "correct" locally |

Design rules:

1. **TTL ≥ 3× p99 operation time**, otherwise normal latency causes takeovers.
2. **TTL ≤ your recovery SLA** (how fast another runner may take over after a crash).
3. **Renew (heartbeat) at ~1/3 TTL**, and *stop working the moment renewal fails* — a holder that
   cannot reach the lock service must not continue.
4. **Heartbeat success is not proof.** A network partition can make the holder think it holds the
   lease while the service has already granted it elsewhere. Only the storage layer can arbitrate —
   which is why you need fencing.

### 40.11 Fencing tokens

A **fencing token** is a monotonically increasing number issued with each lease acquisition. Every
write carries it, and **the storage layer rejects writes whose token is lower than the highest it
has seen**:

```text
worker A acquires lease → token 31
A stalls (GC pause, partition)                     lease expires
worker B acquires lease → token 32
B writes (token 32) → accepted, store remembers max=32
A wakes and writes (token 31) → REJECTED  ← the store, not the lock, enforces this
```

```text
┌────────────┐  acquire  ┌────────────┐   write(data, fence=32)
│  worker B  │──────────▶│ lock svc   │──────────────────────────▶┌──────────────┐
└────────────┘           └────────────┘                           │  storage /   │
┌────────────┐  (stale)                                            │  DB / object │
│  worker A  │── write(data, fence=31) ──────────────────────────▶│  store       │
└────────────┘                            reject if fence < max   └──────────────┘
```

The three layers, and what each one buys you:

| Layer | Mechanism | What it prevents |
|-------|-----------|------------------|
| Lease | TTL + heartbeat | unbounded overlap *if* clocks/network behave |
| **Fencing token** | monotonic counter checked at the store | stale writers **after** expiry/partition |
| Idempotency key | deterministic effect key | duplicate *effects* from retries that are not stale |

> ⚠️ **Hazard.** A lock service's `SET NX PX` (Redis) or session check is **not** fencing. If the
> consumer of the resource does not verify a monotonic token, the lock only *reduces* the chance
> of concurrent writers; it does not eliminate it. This is the well-known objection to naive
> distributed locks, and it applies to any lease-based system without storage-side checks.

Where a real fencing check lives:

- **Database:** `UPDATE jobs SET owner=$1, fence=$2 WHERE id=$3 AND fence < $2` — 0 rows means a
  newer holder owns it.
- **S3/object store:** no native fencing — use a conditional write (`If-Match` on ETag) or make the
  object key include the token and validate at read/commit time.
- **Queue:** delivery-count + visibility timeout gives at-least-once; combine with an idempotent
  handler rather than pretending the queue fences for you.

### 40.12 Replica consistency

What a replica read can and cannot promise:

| Read target | Guarantee | Safe for |
|-------------|-----------|----------|
| Primary | read-your-writes (same txn/session) | preconditions, verification, user-visible read-after-write |
| Replica | eventually consistent; lag is normal | dashboards, lists, analytics, caches |
| Replica **after failover** | may be *behind the old primary* | nothing until you confirm promotion/LSN |

Rules:

1. **Writes and their preconditions come from the primary.** Verifying a version, an existence
   check, or an idempotency key against a replica re-opens every race in 40.6–40.9.
2. **Mark the read intent in code.** A `readFrom: "replica"` on a function that later writes is a
   bug review should catch — make it visible in the signature or a lint rule.
3. **Session stickiness or write-through** for user flows that read immediately after writing.
4. **Failover makes replicas lie.** After promotion, a client that was reading the old primary can
   see data that never existed on the new one; bound it with fencing on writes + idempotency, not
   with hope.
5. **Replication lag is a number, not a binary.** Expose it; route "just wrote, show me" paths to
   the primary when lag exceeds a threshold (commonly ~1 s).

## Worked example

```ts
// A lease + fenced claim for ExportJob. The STORE enforces the fence, not the lock service.
export async function claimExportJob(jobId: string): Promise<FencedClaim | null> {
  const fence = await redis.incr(`fence:export:${jobId}`);   // monotonic per job

  const claimed = await db.query(
    `UPDATE export_jobs
        SET lease_owner = $1, fence = $2, lease_expires_at = now() + interval '30 seconds'
      WHERE id = $3
        AND (lease_expires_at IS NULL OR lease_expires_at < now())
        AND fence < $2`,                                      // ← storage-side fence check
    [workerId, fence, jobId]);
  if (claimed.rowCount === 0) return null;                    // held by someone newer

  return { jobId, fence, token: startHeartbeat(jobId, fence, 10_000) };  // renew every 10 s
}

// Every write downstream carries the fence; a stale worker is rejected by the DB.
export async function writeCheckpoint(claim: FencedClaim, offset: number) {
  const res = await db.query(
    `UPDATE export_jobs SET last_offset = $2, lease_expires_at = now() + interval '30 seconds'
      WHERE id = $1 AND fence = $3`,                          // must match exactly
    [claim.jobId, offset, claim.fence]);
  if (res.rowCount === 0) {
    claim.token.stop();
    throw new FenceLost(claim.jobId, claim.fence);            // STALE: stop immediately
  }
}
```

```text
Failure trace — GC pause past the lease TTL:
  t=0s   A claims: fence=31, lease 30 s, heartbeat every 10 s
  t=30s  A stalls (event-loop blocked / node frozen); lease_expires_at passes
  t=31s  B claims: fence=32 (fence < 32 passes), starts work
  t=34s  A wakes, writes checkpoint WHERE fence=31 → rowCount=0 → FenceLost → A stops
  Result: exactly one writer, no torn checkpoint, no corrupted export file.
```

```sql
-- Replica safety: preconditions always evaluated on the primary, in the writing txn.
BEGIN;
SELECT version FROM settings WHERE tenant_id=$1 FOR UPDATE;   -- primary, locked
UPDATE settings SET version=version+1, ... WHERE tenant_id=$1 AND version=$2;
COMMIT;
```

## Key data / numbers

- Lease TTL guidance: **≥ 3× p99 step duration**, heartbeat at **~1/3 TTL**; common defaults are
  TTL **30–60 s** with a heartbeat every **10 s**.
- Queue **visibility timeouts** (commonly **30–300 s**) are leases in disguise: a message
  redelivered while the first consumer still runs is exactly the stale-holder problem.
- Fencing tokens must be **monotonically increasing per resource** — `redis INCR` on
  `fence:<resource>` is the usual generator; a token from a global counter is fine but coarser.
- Replica lag alerting thresholds: commonly warn **> 1 s**, page **> 5–10 s** (recommendations,
  tune to your workload).
- Postgres: `synchronous_commit`, `wal_receiver` status, and `pg_last_xact_replay_timestamp()`
  give you the actual lag number — read it, do not assume.
- Kubernetes rolling deploys briefly run **two pod versions** — any singleton work item must be
  fenced/idempotent during that overlap.

## Real-world use case — Acme SaaS

`ExportJob` used `SET export:lock <workerId> NX PX 60000` in Redis and wrote directly to S3. During
one node's 40-second freeze (cgroup memory pressure), the lock expired, a second worker started,
and both wrote `exports/<job_id>.csv` — the resulting file interleaved rows from two runs and was
delivered to the customer. The fix: a per-job `INCR` fencing token, a `fence < $new` claim in
Postgres, `WHERE fence = $claim` on every checkpoint write, and S3 keys that include the fence
plus a final conditional `If-Match` on upload completion. They also cut TTL to 30 s with a 10 s
heartbeat so takeover after a real crash took ~30 s instead of minutes. A deliberate `SIGSTOP` test
now produces `FenceLost` in the stale worker and a clean single-writer file every time.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Lease + fencing token | correct even with partitions and pauses | store must verify tokens | any single-writer job over shared state |
| Lease only | simpler | stale overlap possible; correctness is probabilistic | only when duplicates are harmless (then use idempotency instead) |
| Primary-only reads | read-your-writes, safe preconditions | more load on primary | writes, verification, user flows |
| Replica reads | scales reads | stale; unsafe as write input | dashboards, lists, search |
| Advisory/DB locks (`pg_advisory_lock`) | same DB, no extra service | tied to that DB; still lease-like on connection loss | single-DB coordination |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pair every lease with a storage-side fence check | Trust `SET NX` as if it were fencing |
| Stop work the moment renewal/fence fails | Keep writing because "the lock said I own it" |
| Use monotonic clocks for TTL math | Compute TTL from wall clock that NTP can jump |
| Send preconditions and verification to the primary | Verify a version against a replica |
| Treat visibility timeouts as leases | Assume redelivery means the first consumer died |

## Common mistakes

- **Fencing checked only in the lock service** — the store never sees the token, so a stale writer
  still lands.
- **Heartbeat thread keeps running while the work thread is frozen** — the process "holds" a lease
  it cannot actually use safely; tie renewal to work progress.
- **TTL shorter than the operation** — constant takeovers, thrash, duplicate work.
- **Lease release on `finally` only** — a crash skips `finally`; the TTL is the real release.
- **Using a replica's "row missing" as proof of absence** right after a write (40.6 duplicates).
- **Non-monotonic tokens** (timestamps as fences) — clock skew resurrects stale writers.

## Checklist

- [ ] Every lease has a documented TTL, heartbeat interval, and takeover SLA.
- [ ] The resource's storage layer verifies a monotonic fence/token.
- [ ] Workers abort on failed renewal or `rowCount=0` fence checks.
- [ ] Replica reads are labeled and never feed a write or precondition.
- [ ] Visibility-timeout redelivery is assumed concurrent, not sequential.
- [ ] A `SIGSTOP`/partition test proves a stale holder cannot corrupt state.

## Related

- [Workflow Recovery and Long-Running Operations (39.9–39.12)](../39-partial-failures-and-multi-step-operations/01-concepts/04-workflow-recovery-and-long-running-operations.md)
- [Conflict Resolution, Retry Safety, and Corruption (40.13–40.15)](./05-conflict-resolution-retry-safety-and-corruption.md)
- [Worker Crashes and Shutdown During Processing (32.11–32.13)](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)
- [Pools, Partitions, and Duplicate Delivery](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/01-concepts/03-pools-partitions-and-duplicate-delivery.md)
