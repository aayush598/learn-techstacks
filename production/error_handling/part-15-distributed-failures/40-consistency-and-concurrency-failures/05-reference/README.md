# Chapter 40 — Reference

> Part XV · Chapter 40 · Cheat sheets, decision tables, and conflict-handling reference.

## Cheat sheet — concurrency failure signals

| Signal | Meaning | Retryable? | Correct response |
|--------|---------|-----------|------------------|
| `SQLSTATE 40001` | serialization_failure | ✅ yes | whole-transaction retry, fresh reads, 3 attempts |
| `SQLSTATE 40P01` | deadlock_detected | ✅ yes | whole-transaction retry, fresh reads |
| MySQL `1213` | deadlock | ✅ yes | same |
| `SQLSTATE 55P03` | lock_not_available (your `lock_timeout`) | ✅ yes | retry with fresh reads |
| MySQL `1205` | lock wait timeout | ✅ yes | same |
| `SQLSTATE 23505` | unique_violation | ❌ no | duplicate → replay by key or `409` |
| `HTTP 409` (version) | stale version in body | ⚠️ by owner only | refetch + re-apply intent, or `409` to client |
| `HTTP 412` | `If-Match` failed | ⚠️ by owner only | refetch, re-derive ETag, retry |
| Fence lost / lease expired | another owner exists | ❌ no | abort immediately |
| `SQLSTATE 25P02` | in_failed_sql_transaction | ❌ no | the txn is aborted; re-`BEGIN` |
| Ambiguous timeout | outcome unknown | ⚠️ resolve first | read-back before any retry |

## Decision table — which write strategy?

| Situation | Strategy | Mechanism |
|-----------|----------|-----------|
| Commutative op (`+1`, set-add, decrement-if-sufficient) | **single atomic statement** | `UPDATE ... SET n=n+1 WHERE ...` |
| Low/medium contention, human-paced edit | **optimistic** | `version` / `If-Match` → `409`/`412` |
| High contention, tiny critical section | **pessimistic** | `SELECT ... FOR UPDATE`, ascending lock order |
| Work-queue claim (many workers, independent items) | **`FOR UPDATE SKIP LOCKED`** | hands out disjoint rows |
| Need cross-row money invariants | **`SERIALIZABLE` + retry** | accept `40001`, retry whole txn |
| External side effect once | **idempotency key + read-back** | not a locking problem at all |

## Decision table — conflict response

| Client sent | HTTP | Body/code | Client action |
|-------------|------|-----------|---------------|
| Whole object from stale read, body `version` | `409` | `*_VERSION_CONFLICT`, `currentVersion` | refetch, merge, retry |
| `If-Match` with a stale ETag | `412` | `*_VERSION_CONFLICT` | refetch, re-derive, retry |
| No precondition where one is required | `428` | `MISSING_PRECONDITION` | add the precondition |
| Create colliding on a natural key | `409` | `*_EXISTS` | choose different identity / stop |
| Create colliding on an idempotency key still running | `409` | `REQUEST_IN_PROGRESS` (transient) | wait, then retry (replays result) |
| Operation already completed for that key | `200` | stored response replayed | none |
| Row genuinely missing | `404` | `*_NOT_FOUND` | stop |

## Decision table — resolution strategy

| Operation type | Strategy |
|----------------|----------|
| Counter / seat / quota change | atomic single statement (no conflict possible) |
| "Set field to X" from a user | reject with `409` (or merge field-ownership) |
| "Append / add item" | re-apply intent on fresh state |
| Different writers, different fields | field-ownership `PATCH` |
| Bids, auctions, earliest-wins | domain rule, applied explicitly and logged |
| View state, analytics, telemetry | last-writer-wins (acceptable to lose) |
| Money, entitlements, config | never LWW; reject + human |

## Fencing quick reference

```text
acquire(owner) → token T (monotonic, per resource)
write(data, T) → storage accepts iff T > max_seen_token
                 storage records max_seen_token = T
```

| Layer | Guarantee | Does it fence? |
|-------|-----------|----------------|
| Redis `SET NX PX` | at most one holder *if no partition* | no |
| DB lease row + `WHERE fence < $new` | stale writers rejected | **yes** |
| Queue visibility timeout | redelivery after timeout | no (at-least-once) |
| Idempotency key | duplicate *effects* collapse | no (different concern) |

## Key numbers used in this chapter

| Item | Value |
|------|-------|
| Optimistic conflict response | `409` (body version) / `412` (`If-Match`) |
| Precondition required | `428 Precondition Required` |
| Postgres `deadlock_timeout` | 1 s default → `40P01` |
| MySQL `innodb_lock_wait_timeout` | 50 s default (set your own `lock_timeout` to 1–2 s) |
| Concurrency retry budget | 3 attempts, base 25–50 ms, full jitter, whole transaction |
| Lease TTL / heartbeat | TTL ≥ 3× p99; heartbeat ≈ 1/3 TTL (e.g. 30 s TTL, 10 s heartbeat) |
| Replica lag alerting | warn > 1 s, page > 5–10 s (recommended, tune to workload) |
| Constraint SQLSTATEs | `23505` unique, `23514` check, `23503` FK, `23502` not-null |

## Chapter glossary

| Term | Meaning |
|------|---------|
| Race condition | Outcome depends on interleaving of concurrent operations |
| Lost update | A write derived from an old read overwrites a newer value |
| Optimistic concurrency | Detect conflicts by checking version/ETag at commit |
| Pessimistic locking | Prevent conflicts by holding locks during the operation |
| Version conflict | A write's precondition no longer matches the stored state |
| Deadlock | A cycle of transactions each waiting for a lock another holds |
| Fencing token | Monotonic number checked by storage to reject stale writers |
| Lease | A time-bounded lock that expires without holder cooperation |
| Stale read | A read that does not reflect the latest committed write |
| Read-your-writes | Guarantee that a reader sees its own prior writes |
| Conflict resolution | The chosen policy for merging/rejecting conflicting writes |
| Idempotency key | Client-supplied token collapsing duplicate operations to one effect |
| Corruption (here) | Data made internally inconsistent by undetected concurrency |

## Signposts

- DB error classification → [Ch. 22](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
- Transaction retry code → [Ch. 23 practical examples](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
- Idempotency → [Ch. 28](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- Leases in jobs → [Ch. 32 (32.11–32.14)](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)

## Related

- [Chapter 40 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 40 Index](../README.md)
- [Part XV Index](../../README.md)
