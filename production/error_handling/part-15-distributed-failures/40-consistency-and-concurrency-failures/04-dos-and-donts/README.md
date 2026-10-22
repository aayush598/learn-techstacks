# Chapter 40 — Do's and Don'ts

> Part XV · Chapter 40 · All sections

A condensed rule set distilled from the chapter. Use it as a review checklist before any
concurrent write reaches production.

## Races and optimistic control (40.1–40.3)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every editable row a `version`/ETag precondition | Blindly `UPDATE ... SET` the whole row |
| Check `rowCount` on the guarded update | Assume the `UPDATE` matched |
| Return `409` + `currentVersion` (or `412` for `If-Match`) | Return `500` for a stale write |
| Retry by re-reading and re-applying intent | Retry the stale payload with the old version |
| Count conflicts per endpoint as a metric | Treat contention as an invisible shame |

## Locks, deadlocks, and duplicates (40.4–40.7)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set `lock_timeout` (1–2 s) and treat expiry as retryable | Wait 50 s (MySQL default) and call it reliable |
| Lock multi-row sets in ascending, documented order | Lock in UI/array order |
| Retry `40001`/`40P01`/`1213` as whole transactions | Retry only the failed statement |
| Use unique constraints for "create exactly once" | `SELECT`-then-`INSERT` without a constraint |
| Treat `23505` as a duplicate detector, then replay or `409` | Retry `23505` as transient |
| Do network I/O outside transactions | Hold row locks across an HTTP call |

## Lost updates and stale reads (40.8–40.9)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate a write against the state it came from | Derive a write from a replica or cache read |
| Read-your-writes from the primary after a write | Read the row back from a lagging replica |
| Give background jobs and webhooks preconditions too | Assume only humans race |
| Use integer versions, not timestamps | Rely on second-precision `updated_at` |
| Distinguish `404` from `409` | Report a missing row as a conflict |

## Leases, fencing, replicas (40.10–40.12)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pair every lease with a storage-side fencing token | Trust Redis `SET NX` as if it were fencing |
| Set TTL ≥ 3× p99 work time; heartbeat ~1/3 TTL | Let the lease expire during normal work |
| Abort when renewal or the fence check fails | Keep writing because "the lock said I own it" |
| Send preconditions and verification to the primary | Verify a version against a replica |
| Assume visibility-timeout redelivery is concurrent | Assume redelivery means the first consumer died |

## Resolution, retry safety, corruption (40.13–40.15)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the resolution strategy per conflict type | Let the second `UPDATE` win by accident |
| Keep one owner of retries per operation | Retry in repository *and* service |
| Put critical invariants in `CHECK`/`UNIQUE` constraints | Trust application `if` checks for money |
| Make commutative ops single atomic statements | Read-modify-write in application code |
| Run reconciliation and alert on any drift | Assume prevention layers never leak |
| Use last-writer-wins only for disposable data | LWW over config, balances, or entitlements |

## Anti-patterns in the wild

1. **The Cosmetics** — a `version` column that no `UPDATE` actually checks in its `WHERE`.
2. **The Infinite `409`** — a client retrying the same stale body until it gives up with a worse
   error.
3. **The Lock & Call** — `FOR UPDATE` held across an external API call; pool exhaustion follows.
4. **The Pair of Retries** — repository and service both retry `40001`, multiplying load 9×.
5. **The Rumored Lock** — a lease with no fencing token; the stale holder still writes.
6. **The Sticky Replica** — verifying a version or existence against a lagging replica.
7. **The Silent Merge** — LWW over a settings object nobody agreed to make disposable.
8. **The Orphaned Counter** — application-side `if (n < limit) n++` with no constraint behind it.

## Chapter checklist

- [ ] Every editable/multi-writer row has a version or `If-Match` precondition.
- [ ] Every guarded write checks `rowCount`; conflicts map to `409`/`412`/`404` deliberately.
- [ ] `lock_timeout` set; deadlock/serialization retries are whole-transaction, bounded, jittered,
      and single-owned.
- [ ] Every "create" has a unique constraint and an idempotency path; `23505` is classified.
- [ ] Distributed locks carry fencing tokens checked by the storage layer.
- [ ] No write or precondition is derived from a replica/cache read.
- [ ] Each conflict type has a named resolution strategy and a metric.
- [ ] Critical invariants are enforced by DB constraints, with reconciliation as the safety net.

## Related

- [Chapter 40 Reference](../05-reference/README.md)
- [Chapter 40 Index](../README.md)
- [Part XVII — Error Handling in Architecture and Code Organization](../../../part-17-organization/README.md)
