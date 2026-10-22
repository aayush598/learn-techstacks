# Chapter 23 — Do's and Don'ts

> Part IX · Chapter 23 · All sections

Review rules for transaction and rollback error handling.

## Boundaries and atomicity

| ✅ Do | ❌ Don't |
| ----- | -------- |
| One transaction per aggregate | Wrap five aggregates in one long transaction |
| Keep transactions short (< 100 ms on hot paths) | Await a user or an HTTP call inside `BEGIN` |
| Put invariants in SQL predicates or locks | `SELECT` then `UPDATE` under `READ COMMITTED` |
| Use sagas for multi-service work | Hold a transaction across Stripe/S3 |
| Set `idle_in_transaction_session_timeout` | Leave transactions open between requests |

## Commit and rollback

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat commit-time connection loss as **unknown** | Assume a failed `COMMIT` rolled back |
| Resolve unknown outcomes by reading a marker | Blind-retry a possibly committed write |
| Close broken connections | Return them to the pool |
| Use savepoints for per-item recovery | Keep querying in `25P02` |
| Return explicit partial results | Report partial success as full success |

## Retry

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry `40001`/`40P01`/`1213` as a **whole transaction** | Retry the failing statement |
| Re-read state inside each attempt | Reuse stale `version`/`balance` |
| Cap attempts (~3) with jittered backoff | Infinite or fixed-delay retries |
| Require idempotency before retrying writes | Retry `23505`, `23503`, `23514` |
| Own retries in exactly one layer | Retry in repository *and* service |

## Ambiguity and idempotency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model `unknown` as a third outcome | Collapse it into success/failure |
| Commit the idempotency key with the effect | Write the key after commit |
| Reuse the same key across attempts | Generate a new key per attempt |
| Resolve from the **primary** | Read a replica to decide |
| Record provider `unknown` state | Guess whether a charge applied |

## After commit, outbox, compensation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write events to an outbox in the same txn | Publish before commit |
| Publish after commit via a relay | Publish inline with no retry |
| Dedupe consumers on `event_id` | Assume exactly-once |
| Mark the outbox row after publish | Delete it before publishing |
| Make compensation idempotent and audited | Refund/release unconditionally |
| Choose one owner per datum | Dual-write Postgres and Redis "atomically" |

## Anti-patterns in the wild

1. **The phantom rollback** — assumes a failed commit did nothing; double-charges.
2. **The statement retry** — retries `40001` inside a dead transaction.
3. **The orphan charge** — charges before the order is committed.
4. **The lost event** — commits, then publishes with no retry.
5. **The phantom event** — publishes, then the transaction rolls back.
6. **The duplicate refund** — compensation without a state guard or idempotency key.
7. **The stale retry** — reuses the version read before the conflict.
8. **The healed connection** — puts a broken socket back in the pool.

## Chapter checklist

- [ ] Every unit of work has an explicit, short boundary.
- [ ] No external calls inside a transaction.
- [ ] Commit ambiguity is a named state with a resolver.
- [ ] Write retries are whole-transaction, re-reading, capped, and jittered.
- [ ] Idempotency keys commit with the effect.
- [ ] Events go through an outbox; consumers dedupe.
- [ ] Compensation is idempotent and state-guarded.

## Related

- [Chapter 23 Reference](../05-reference/README.md)
- [Chapter 22 Do's and Don'ts](../../22-database-error-classification/04-dos-and-donts/README.md)
- [Error Handling Patterns and Anti-Patterns (Ch. 46)](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
