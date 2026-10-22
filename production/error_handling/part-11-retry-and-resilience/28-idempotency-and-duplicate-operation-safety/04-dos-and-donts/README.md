# Chapter 28 — Do's and Don'ts

> Part XI · Chapter 28 · All sections

A condensed rule set distilled from the chapter. Use it as an idempotency review checklist.

## Keys

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Generate one key per logical operation | Generate a key per attempt or click |
| Scope keys to `(tenant, operation)` | Use a global key namespace |
| Use UUID/ULID opaque strings | Derive keys from mutable input |
| Accept the key via `Idempotency-Key` | Trust a key as authorization |
| Reuse the key at the provider too | Send a different provider key |

## Detection and storage

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce a unique `(scope, key)` index | `SELECT` then `INSERT` |
| Store status + body + resource id | Store only "seen" |
| Store a canonical payload hash | Hash raw bytes with timestamps |
| Commit key + local effect atomically | Update the key after commit |
| Use an outbox for external calls | Assume a DB tx covers the provider |

## Concurrency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return `409` for in-progress | Let the loser execute too |
| Optionally wait briefly, then replay | Block forever on the first request |
| Use a lease + sweeper | Leave crashed keys `in_progress` |
| Derive leases from P99 duration | Use the average |

## Replay

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Replay the original status code | Return a fresh `200` |
| Replay the original body | Regenerate ids/timestamps |
| Mark replays with a header | Make replays indistinguishable silently |
| Reject payload mismatch with `422` | Overwrite the record |
| Return `202` for pending outcomes | Report unknown as done |

## TTL and failures

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set TTL ≥ retry + reconciliation windows | Expire keys before retries finish |
| Persist terminal failures | Delete keys on failure |
| Model `unknown` explicitly | Collapse unknown into failed |
| Reconcile by correlation id | Retry blind after a timeout |
| Alert on effects without key rows | Assume the ledger is complete |

## By domain

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key payments by order | Key payments randomly |
| Key refunds by refund request | Reuse the charge key for refunds |
| Key job steps by `job_id:step:input_hash` | Key only by job id |
| Dedup webhooks on event id | Dedup on payload |
| Ack webhooks before long work | Process synchronously |
| Propagate keys across services | Regenerate at each boundary |
| Derive child keys deterministically | Use random child keys |

## Anti-patterns in the wild

1. **The Fresh Key** — regenerates the key on every retry, guaranteeing duplicates.
2. **The Read-Write Race** — checks for a key, then inserts, under concurrency.
3. **The Boolean** — records only "seen," so duplicates get an empty response.
4. **The Amnesiac Key** — TTL shorter than the retry window.
5. **The Silent Overwrite** — accepts a reused key with a different payload.
6. **The Stuck Claim** — no lease, so a crash blocks the key forever.
7. **The Optimistic Failure** — marks "failed" when the outcome is unknown.

## Chapter checklist

- [ ] Every non-idempotent write has a dedup key or natural key.
- [ ] Keys are stable across retries and scoped per tenant.
- [ ] A unique constraint enforces key uniqueness.
- [ ] Key + local effect commit together.
- [ ] External effects use an outbox or reconciler.
- [ ] Concurrent duplicates are rejected or waited on.
- [ ] Completed duplicates replay the original response.
- [ ] Payload mismatch is rejected with `422`.
- [ ] TTL covers retry and reconciliation windows.
- [ ] Webhooks dedupe on event id before processing.

## Related

- [Chapter 28 Reference](../05-reference/README.md)
- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Part XVII — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
