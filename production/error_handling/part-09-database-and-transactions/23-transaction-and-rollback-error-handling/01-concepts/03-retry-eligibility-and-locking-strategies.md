# Retry Eligibility and Locking Strategies (23.7–23.10)

> Part IX · Chapter 23 · Sections 23.7–23.10 · _Estimated reading time: 22 min_
> **Prerequisite:** [Commit, Rollback, and Savepoints](./02-commit-rollback-and-savepoints.md)

## In one sentence

Retry is allowed only when the failure is **transient, the transaction is the unit of retry, and
re-execution is side-effect-safe**; locking strategy decides how often you need that retry in the
first place.

## Why this matters in production

Retry is the most commonly over-applied resilience technique. Retrying a `23505` creates
duplicates; retrying inside an aborted transaction fails instantly; retrying a non-idempotent
charge double-bills. Meanwhile, choosing the wrong lock strategy creates the conflicts you then
retry: optimistic locking without a version check silently loses updates, and pessimistic locking
without a consistent order deadlocks under load. **Eligibility is a table; locking is a design
choice.**

## Core concept

### 23.7 Retry eligibility

| Condition | Required |
| --------- | -------- |
| Error class is transient (`40001`, `40P01`, `1213`, `55P03`, `08xxx`, `53300`) | yes |
| Retry scope is the **whole transaction** | yes |
| Operation is **idempotent** or guarded by an idempotency key | yes |
| Attempts are **capped** and **jittered** | yes |
| Failure is not the result of invalid data or a bug | yes |

If any answer is "no", **do not retry** — translate and return.

```text
retryable?  ── no ──▶ translate (permanent) ──▶ 409/422/500
     │ yes
     ▼
idempotent? ── no ──▶ add key/unique marker first
     │ yes
     ▼
attempt < max? ── no ──▶ return exhausted error (409/503)
     │ yes
     ▼
backoff + jitter → BEGIN again (re-read state)
```

### 23.8 Deadlock retry

Deadlocks (`40P01`, MySQL `1213`) are **normal** under concurrent writes. The database picks a
victim and aborts it; your job is to retry that transaction with a fresh snapshot. Two rules:

1. **Retry from `BEGIN`** — never re-issue the statement in the aborted transaction.
2. **Reduce the deadlock rate structurally** — consistent lock ordering, shorter transactions,
   indexes that avoid gap locks.

### 23.9 Optimistic conflicts

Optimistic concurrency uses a **version column** (or `updated_at`) and a conditional `UPDATE`:

```sql
UPDATE projects
   SET name = $1, version = version + 1
 WHERE id = $2 AND version = $3;
-- rowCount = 0 → someone else won; re-read and decide (retry or 409/412)
```

A zero-row update is **not** a database error — it is a detected conflict. Map it to `409` (or
`412` at the HTTP boundary) and let the caller decide whether to re-read. Retrying *the same
stale version* can never succeed.

### 23.10 Pessimistic locking

`SELECT ... FOR UPDATE` takes a row lock for the duration of the transaction:

| Clause | Behavior | Use |
| ------ | -------- | --- |
| `FOR UPDATE` | exclusive, blocks writers and other `FOR UPDATE` | read-modify-write |
| `FOR NO KEY UPDATE` | weaker; does not block FK checks | Postgres, high concurrency |
| `FOR SHARE` | shared; blocks writers | reference reads that must not change |
| `FOR UPDATE SKIP LOCKED` | skip locked rows | **queue/outbox relay** |
| `FOR UPDATE NOWAIT` | fail immediately if locked | latency-sensitive paths |

Pessimistic locking is correct but must be **short** and **ordered**. Keep lock acquisition in
the same order everywhere (e.g. by primary key) to avoid cycles.

## How it works (mechanics)

1. Classify the error; if not transient, stop.
2. Decide idempotency: natural key, unique constraint, idempotency table, or read-back marker.
3. Roll back (or let the wrapper roll back).
4. Sleep `min(cap, base * 2^attempt) * jitter`.
5. Re-enter the **transaction function**, which re-reads all state it depends on.
6. After `maxAttempts`, return a **meaningful exhausted** error (not the raw driver error).

## Worked example

```go
func (s *Service) Transfer(ctx context.Context, from, to int64, cents int64) error {
    const maxAttempts = 3
    for attempt := 1; attempt <= maxAttempts; attempt++ {
        err := s.db.WithTx(ctx, func(tx *sql.Tx) error {
            // Lock in deterministic order to avoid deadlocks.
            first, second := from, to
            if first > second { first, second = second, first }

            if _, err := tx.ExecContext(ctx,
                `SELECT id FROM accounts WHERE id IN ($1,$2) ORDER BY id FOR UPDATE`,
                first, second); err != nil { return err }

            if _, err := tx.ExecContext(ctx,
                `UPDATE accounts SET balance = balance - $1 WHERE id = $2`, cents, from); err != nil { return err }
            if _, err := tx.ExecContext(ctx,
                `UPDATE accounts SET balance = balance + $1 WHERE id = $2`, cents, to); err != nil { return err }
            return nil
        })
        if err == nil { return nil }
        if !isRetryableConflict(err) { return err }       // 40001, 40P01, 1213
        if attempt == maxAttempts { return exhausted(err) }
        sleep(ctx, backoff(attempt))                       // 20–80ms + jitter
    }
    return nil
}
```

## Key data / numbers

- Retryable transaction codes: **`40001`**, **`40P01`**, MySQL **`1213`**, **`55P03`**/`1205`
  (lock timeout). Class `08` and `53300` are retryable but need **connection-level** backoff.
- Typical retry budget: **3 attempts**; base delay **20–50 ms**, exponential, **full jitter**.
- `deadlock_timeout` (Postgres) default **1 s**; MySQL `innodb_lock_wait_timeout` default **50 s**
  (lower it for request paths).
- Optimistic version check returning **0 rows** means conflict, not "not found" — distinguish by
  a follow-up `SELECT` or by using `RETURNING`.
- `SKIP LOCKED` requires Postgres **9.5+** / MySQL **8.0+**.

## Real-world use case — Acme SaaS

Acme's `ExportJob` processed checkpoints with `SELECT ... FOR UPDATE` and retried `23505` "just
in case". Under load, two workers deadlocked constantly; the retry of the unique violation
produced duplicate checkpoint rows, and duplicate checkpoints caused duplicated export rows.
The fix: **one** retry policy for `40001`/`40P01` (whole transaction, 3 attempts), **no retry**
for `23505` (the checkpoint row is upserted instead), and `SKIP LOCKED` on the export queue.
Deadlock recoveries became invisible, duplicate checkpoints went to zero, and export workers
stopped colliding.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Retry on `40001`/`40P01` | handles normal contention | work re-executed | default for writes |
| Optimistic versioning | no locks, scales reads | caller must resolve `409`/`412` | low-contention updates |
| Pessimistic `FOR UPDATE` | simple mutual exclusion | contention, deadlock risk | short critical sections |
| `SKIP LOCKED` queue | parallel consumers, no blocking | not FIFO | outbox/job relays |
| No retry + `409` | predictable | users see conflicts | interactive edits |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry only transient classes | Retry `23505`, `23503`, `23514`, `42xxx` |
| Retry the whole transaction | Retry a single statement |
| Re-read state inside the retry | Reuse pre-abort values |
| Cap attempts and jitter delays | Fixed 1 s sleep, unbounded loops |
| Lock rows in a deterministic order | Lock in request order |
| Treat 0-row optimistic update as conflict | Treat it as success |

## Common mistakes

- **Retrying a unique violation** — duplicates or permanent loop.
- **Retrying with the same `version`** — always conflicts.
- **Infinite retries** — hides contention and exhausts the pool.
- **`FOR UPDATE` in a long transaction** — blocks every writer, produces lock timeouts.
- **`SKIP LOCKED` for user-facing reads** — returns an incomplete view.

## Checklist

- [ ] A retry table exists and is keyed on error class, not message.
- [ ] Idempotency is proven before any retry of a write.
- [ ] Retries re-enter `BEGIN` and re-read state.
- [ ] Attempts are capped and delays are jittered.
- [ ] Lock order is consistent; `SKIP LOCKED` is used for queue-style reads.
- [ ] Optimistic 0-row updates map to `409`/`412`.

## Related

- [Ambiguous Commits and Idempotent Retries (23.11–23.14)](./04-ambiguous-commits-and-idempotent-retries.md)
- [Retrying 40001 and 40P01 in Code](../03-practical-examples/01-retrying-40001-and-40p01.md)
- [Conflicts, Locks, and Timeouts (22.9–22.13)](../../22-database-error-classification/01-concepts/03-conflicts-locks-and-timeouts.md)
- [Retry Policies (Ch. 27)](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
