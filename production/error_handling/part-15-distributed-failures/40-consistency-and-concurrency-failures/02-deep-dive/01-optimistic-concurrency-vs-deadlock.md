# Optimistic Concurrency vs Deadlock (Mechanics)

> Part XV · Chapter 40 · Sections 40.2, 40.3, 40.5 (mechanics) · _Estimated reading time: 28 min_
> **Prerequisite:** [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](../01-concepts/01-races-optimistic-control-and-version-conflicts.md)

## In one sentence

**Optimistic control** trades a lock wait for a possible retry by checking a version at commit,
while a **deadlock** is what pessimistic locking looks like when two transactions acquire locks in
opposite orders — the database detects the cycle, aborts one victim, and *both* strategies end in
"retry the whole transaction," which is why defending one defense is not enough.

## Why this matters in production

Choosing between OCC and locking is one of the few concurrency decisions that changes your p99
under load: OCC wastes work but never blocks, locking blocks but never wastes a conflict. Getting
this wrong produces two recognizable incidents — a hot row that refuses to accept writes during a
retry storm (too optimistic), or a lock convoy where p99 collapses to the lock timeout floor (too
pessimistic). And because both can *also* deadlock or conflict, the retry wrapper must handle both
classes regardless of which you chose. This file is the mechanics behind the decision.

## The two strategies side by side

```text
OPTIMISTIC (version)                       PESSIMISTIC (row lock)
─────────────────────                      ──────────────────────
BEGIN                                      BEGIN
  READ row (v=7)                             SELECT ... FOR UPDATE   ← blocks here
  compute                                    compute
  UPDATE ... WHERE version=7                 UPDATE ...
  ├─ 1 row → COMMIT                          COMMIT  (releases lock)
  └─ 0 rows → retry/409                    (no conflicts — you serialize)
COMMIT
```

| Property | Optimistic | Pessimistic |
|----------|-----------|-------------|
| Blocks competing writers? | no | yes |
| Wasted work on conflict | yes (compute redone) | no |
| Deadlock risk | none from this row (no lock held) | **yes** (lock ordering matters) |
| Lock wait / convoy risk | none | yes |
| Pool pressure | low | high (waiters hold connections) |
| Latency under low contention | lowest | slightly higher (lock/unlock) |
| Latency under high contention | retry loops | predictable waits, then timeouts |
| Client involvement | must handle `409` | transparent |
| Best at | low–medium contention, human-paced | high contention, very short critical sections |

## Mechanics of OCC

The commit-time check is a **compare-and-swap at the row level**:

```sql
UPDATE accounts
   SET balance = $2, version = version + 1
 WHERE id = $1 AND version = $3;    -- CAS: succeeds iff nothing changed since read
```

Postgres/MySQL implement this as a normal update under the row lock; the difference from
`FOR UPDATE` is *timing* — the lock is held for microseconds at the `UPDATE`, not across the
application's compute. Consequences:

- **First write wins; second gets zero rows** → your code must translate that to `409`.
- **Two attempts may conflict repeatedly** on a hot row — measure and consider batching
  (`SET n = n + k`) or sharding a counter across rows.
- **Phantom-adjacent conflicts** (insert/delete changing a predicate) are *not* caught by a version
  column — those need `SERIALIZABLE` (`40001`) or explicit locks.

### The retry loop that keeps OCC honest

```python
def occ_update(pool, row_id, expected_version, intent, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        with pool.transaction() as tx:                       # READ is INSIDE the txn
            row = tx.read(row_id)                            # fresh every attempt
            new = intent(row)                                # apply user intent to NEW state
            n = tx.execute(
                "UPDATE t SET val=%s, version=version+1 WHERE id=%s AND version=%s",
                (new, row_id, row.version))
            if n == 1:
                return new                                   # committed
            # conflict: loop and read again
        time.sleep(random.uniform(0, 25e-3 * 2 ** (attempt - 1)))
    raise DomainError("VERSION_CONFLICT", http=409)
```

> ⚠️ **Hazard.** `intent` must be a **function of the current row** ("approve the pending order",
> "+1 seat"), not a closure over the originally-read row. Applying a stale snapshot inside the
> retry loop reproduces the lost update with extra steps.

## Mechanics of deadlocks

A deadlock is a cycle in the wait-for graph:

```text
wait-for graph
   T1 ──waits for lock held by──▶ T2
   ▲                              │
   └────waits for lock held by────┘        cycle ⇒ deadlock (no one can proceed)
```

How the database resolves it:

| Step | Postgres | MySQL/InnoDB |
|------|----------|--------------|
| Detection | wait-for graph scan after `deadlock_timeout` (**1 s** default) | cycle detection on lock wait **immediately** |
| Victim | one transaction, its choice | one transaction, weighted by work done |
| Victim error | **`40P01`** `deadlock_detected` | **`1213`** `ER_LOCK_DEADLOCK` |
| State after | victim aborted; **transaction must be rolled back**, `25P02` on further statements | victim rolled back |
| Correct client action | retry the **whole transaction**, fresh reads | same |

Why deadlocks are *normal*:

- Any two transactions touching **two or more shared rows** in potentially different orders can
  cycle. Under enough concurrency, "unlikely" becomes "hourly."
- **The DB chooses the victim, not you.** Even a carefully ordered transaction can be the victim,
  so the retry handler is mandatory for any multi-row transaction.

Prevention, best to worst:

1. **Eliminate the multi-row transaction**: one atomic `UPDATE` (e.g. `UPDATE ... SET n=n+1`,
   `UPDATE ... WHERE`, `INSERT ... ON CONFLICT`) has a single lock point and cannot cycle.
2. **Enforce a total lock order**: always lock rows by ascending id; document it. This removes
   *most* cycles for a known row set.
3. **Shorten transactions**: acquire locks late, release early, no I/O while holding them.
4. **Set `lock_timeout`** so a *wait* (not a cycle) also fails fast as `55P03`, retryable.
5. **Lower isolation** only where the business tolerates it — `SERIALIZABLE` trades deadlocks for
   `40001`s (same retry shape, more of them).

```sql
-- Total lock order: lock BOTH accounts deterministically, ascending.
WITH locked AS (
  SELECT id FROM accounts WHERE id IN ($1, $2) ORDER BY id FOR UPDATE
)
SELECT 1 FROM locked;     -- both rows held; the transfer can no longer deadlock with a peer
```

```text
Two transfers that deadlock without ordering:
  A→B: locks account A, then wants B
  B→A: locks account B, then wants A      ⇒ cycle ⇒ one gets 40P01

With ascending-id ordering, both lock min(A,B) first: one waits; the other completes; no cycle.
```

## Choosing between them (the decision)

```text
Is the operation commutative?
├─ yes → single atomic statement (SET n=n+1, ON CONFLICT). Neither lock nor version needed.
└─ no → how hot is the row?
        ├─ low/medium contention (few % conflicts) → OPTIMISTIC (version + 409)
        └─ high contention, very short critical section → PESSIMISTIC (FOR UPDATE)
              └─ but ALWAYS also: consistent lock order, lock_timeout, retry on 40P01
              └─ and if the lock is held across a network call → redesign. No exceptions.
```

The hybrid that most production systems land on:

- **Optimistic by default** (no blocking, scales, `409` is client-actionable).
- **Pessimistic only for tiny, hot, multi-row invariants** (e.g. inventory reservation across two
  rows, transfer between two accounts) — with a total lock order and a whole-transaction retry.
- **Atomic single statements wherever the operation is commutative** — the cheapest correct answer.

## Key data / numbers

- Postgres `deadlock_timeout` **1 s** (detection scan cadence), `lock_timeout` **0 = wait forever**
  → always set **1–2 s**. MySQL `innodb_lock_wait_timeout` default **50 s**.
- Victim SQLSTATEs: **`40P01`** deadlock, **`40001`** serialization, **`55P03`** lock timeout,
  **`25P02`** `in_failed_sql_transaction` (what you get if you keep using an aborted txn), MySQL
  **`1213`**, **`1205`**.
- Retry budget for both classes: **3 attempts**, base **25–50 ms**, full jitter, whole transaction.
- OCC conflict cost ≈ one wasted read+compute (+ one extra round trip); pessimistic wait cost ≈
  lock hold time; retry storm cost ≈ **multiplied** work under peak load — the reason hot rows
  need a different design, not more retries.
- `FOR UPDATE` variants: `NOWAIT` (fail immediately → `55P03`-like), `SKIP LOCKED` (work-queue
  pattern, avoids contention entirely by handing out different rows).

## Real-world use case — Acme SaaS

Acme had two separate concurrency incidents on the same `accounts`-style table (tenant credit
balances):

1. **Too optimistic:** a hot tenant's `balance` was read-modify-written with a version check. Under
   a billing batch, conflict retries consumed ~9% of request CPU and p99 hit 1.4 s. Fix: single
   atomic `UPDATE ... SET balance = balance - $2 WHERE balance >= $2` — the operation was
   commutative, and conflicts vanished.
2. **Too pessimistic:** an "apply credit across two balances" path used `FOR UPDATE` on both rows
   in the order the UI sent them, deadlocking several times per hour at `40P01` during peak.
   Waiters held pool connections, and one deadlock wave exhausted the pool. Fix: ascending-id lock
   order + `lock_timeout='2s'` + whole-transaction retry; deadlocks fell from ~40/hour to a
   handful, and none surfaced to users because the retry wrapper absorbed them within 50 ms.

The lesson both times: **the choice was per operation**, not global.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Single atomic statement | no conflicts, no locks held | only for commutative ops | counters, quotas, conditional decrements |
| Optimistic + `409` | scales, client-actionable, no waits | retry loops on hot rows | default; most APIs |
| Pessimistic `FOR UPDATE` | one winner, no wasted work | waits, deadlocks, pool pressure | tiny hot multi-row invariants |
| `FOR UPDATE SKIP LOCKED` | no contention; queue semantics | ordering not guaranteed | job/claim queues |
| `SERIALIZABLE` + retry | strongest invariants | more `40001` conflicts | money invariants across rows |
| "No strategy" | none | corruption | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make commutative ops a single atomic statement | Read-modify-write in application code |
| Decide OCC vs locking per operation | Pick one strategy for the whole codebase by taste |
| Lock multi-row sets in a documented ascending order | Lock in UI/array order |
| Retry the whole transaction on `40P01`/`40001`/`1213` | Retry the single failed statement |
| Set `lock_timeout` so waits fail fast and retry | Wait 50 s and exhaust the pool |
| Re-read state inside every retry | Reuse a captured snapshot |

## Common mistakes

- **"We use OCC so we cannot deadlock"** — true for the version column, false for the rest of the
  transaction's locks.
- **`FOR UPDATE` held across an HTTP/LLM call** — the single most common source of pool exhaustion
  and convoying.
- **Catching `40P01` but continuing the same transaction** — you get `25P02` and lose the retry.
- **Two retry layers** (`40001` handled in repository *and* service) — 3×3 attempts under peak load.
- **Ascending lock order only in the new code** — one legacy path in reverse order re-introduces
  the cycle.
- **Treating `1213`/`40P01` as 5xx to the user** — they are transient; retry internally first.

## Checklist

- [ ] Every multi-row write path has a chosen strategy (atomic / OCC / lock) and says why.
- [ ] Locked rows are acquired in ascending id order everywhere.
- [ ] `lock_timeout` (1–2 s) is set; expiry is classified retryable.
- [ ] `40P01`, `40001`, `1213` retry the whole transaction with fresh reads, bounded + jittered.
- [ ] Exactly one layer owns these retries.
- [ ] No transaction holds locks across network I/O.
- [ ] Hot rows are identified; commutative operations use single statements.
- [ ] Deadlock/conflict rates and retry counts are monitored.

## Related

- [Conflict Resolution, Retry Safety, and Corruption (40.13–40.15)](../01-concepts/05-conflict-resolution-retry-safety-and-corruption.md)
- [Optimistic Locking with a Version Column — worked example](../03-practical-examples/01-optimistic-locking-with-version-column.md)
- [Retry Eligibility and Locking Strategies (23.7–23.10)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/01-concepts/03-retry-eligibility-and-locking-strategies.md)
- [Retrying 40001 and 40P01 in Code](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
