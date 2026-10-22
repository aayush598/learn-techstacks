# Conflict Resolution, Retry Safety, and Preventing Corruption (40.13–40.15)

> Part XV · Chapter 40 · Sections 40.13–40.15 · _Estimated reading time: 22 min_
> **Prerequisite:** [Lost Updates, Stale Reads, and Conflicting Writes (40.8–40.9)](./03-lost-updates-stale-reads-and-conflicting-writes.md)

## In one sentence

Once a conflict is *detected*, you must choose a **resolution strategy** (reject, merge, last-
write, re-apply), and once you *retry*, you must prove the retry is **safe** — because the
alternative is not an error, it is **silent corruption** that no monitor will ever show you.

## Why this matters in production

Detection without resolution just moves the failure: a `409` that clients never handle, a deadlock
retry that re-sends a stale payload, a "conflict resolved by last writer wins" policy that quietly
deleted a colleague's edit. And a retry that is unsafe under concurrency — non-idempotent effects,
captured-from-the-old-state values, compensation fired twice — converts a transient race into
permanent damage. This file closes the loop: **detect (40.1–40.9) → resolve → retry safely →
verify nothing is corrupted.**

## Core concept

### 40.13 Conflict resolution

| Strategy | Mechanism | Guarantees | When |
|----------|-----------|------------|------|
| **Reject** (`409`/`412`) | fail the losing writer; let a human/client decide | no silent loss | default; user edits, whole-object writes |
| **Re-apply intent** | re-read, re-run the operation on the new state | correct for commutative ops | increments, counters, append ops |
| **Field merge** | each writer owns fields; merge on write | concurrent different-field edits succeed | settings/profiles/multi-writer documents |
| **CRDT / commutative ops** | mathematically mergeable updates | no conflicts by construction | counters, sets, presence, collaborative editing |
| **Last-writer-wins (LWW)** | timestamp decides | total order, **loses data** | only for disposable data (view state, telemetry) |
| **Domain-specific resolution** | business rule (higher bid wins, earliest wins, sum) | correct by business semantics | pricing, inventory, auctions, quotas |

Choosing, in one decision rule:

```text
Is the operation commutative (order doesn't matter: n=n+1, set add)?
├─ yes → make it atomic in the store (SET n=n+1 / ON CONFLICT) → no conflict at all
└─ no  → does the domain define who wins?
         ├─ yes (business rule) → apply it explicitly, log the resolution
         └─ no  → REJECT with 409/412 + current state; let the client merge
Last-writer-wins only for data you would not mind losing.
```

⚠️ **Hazard.** "Resolution" that happens implicitly — the second `UPDATE` simply overwriting the
first — is not a strategy, it is an accident. Every conflict resolution should be **nameable** in
the design doc and **countable** in metrics.

### 40.14 Retry safety under concurrency

A retry is safe only if all four hold:

```text
SAFE RETRY = idempotent effect
           ∧ fresh state read (no captured stale values)
           ∧ bounded attempts + backoff
           ∧ single owner of the retry decision (no two layers retrying)
```

| Question | If the answer is "no" |
|----------|-----------------------|
| Is the effect idempotent (key/unique/conditional)? | do not retry — resolve by read-back first |
| Does the attempt re-read everything it depends on? | it will conflict again, deterministically |
| Is it bounded with jitter? | retry storm / amplification |
| Is exactly one layer retrying? | n×m attempts, amplified load at the worst time |
| Is the classification correct (`40001`/`40P01` yes, `409` no* ) | either silent failure or permanent-error loops |

\* `409` *can* be retried — but only by a component that re-reads and re-applies intent, never by
a transparent transport retry.

Concurrency-specific retry rules:

1. **Deadlock/serialization (`40P01`, `40001`, `1213`)** → retry the *whole transaction* with fresh
   reads; up to **3 attempts**, full jitter.
2. **Version conflict (`409`/`412`)** → not a transport retry; the *writer with intent* must
   refetch, re-apply, re-send.
3. **Duplicate (`23505`)** → replay the stored result or return `409`; never "try again."
4. **Fence lost / lease expired** → do **not** retry; another owner exists.
5. **Ambiguous outcome** → read-back resolution before any retry decision.

### 40.15 Preventing corruption

Corruption is a *state* problem, so prevention is structural:

| Structural guard | What it stops |
|------------------|---------------|
| **Constraints** (`UNIQUE`, `CHECK`, `NOT NULL`, FK) | illegal states no application code enforces consistently |
| **Version/`If-Match` preconditions** | lost updates, blind overwrites |
| **Single-writer + fencing** | torn writes from overlapping holders |
| **Invariants in the DB** (`CHECK (n >= 0)`, `balance = ...`) | arithmetic that application races get wrong |
| **Idempotency keys + read-back** | duplicate side effects |
| **Atomic read-modify-write in one statement** | read-modify-write races entirely |
| **Reconciliation** (periodic invariant check) | drift that slipped past everything else |

The layered model:

```text
 ┌─────────────────────────────────────────────────────┐
 │ application: classify, resolve, retry safely        │
 ├─────────────────────────────────────────────────────┤
 │ protocol:    versions, If-Match, idempotency keys   │
 ├─────────────────────────────────────────────────────┤
 │ storage:     UNIQUE / CHECK / FK / NOT NULL         │  ← the last line
 ├─────────────────────────────────────────────────────┤
 │ operations:  reconciliation, invariants, audits     │  ← catches what leaked
 └─────────────────────────────────────────────────────┘
```

**Trust the bottom layers more than the top.** An application-level `if (balance >= amount)` is a
race; `CHECK (balance >= 0)` is not. If a constraint would be *impossible* to violate, you do not
need the `if`; if it is possible, you needed the constraint anyway.

## Worked example

```ts
// Resolution + retry safety in one place: a retry policy that KNOWS what it may retry.
type RetryClass =
  | "transaction_conflict"   // 40001, 40P01, 1213 → whole-txn retry, fresh reads
  | "version_conflict"       // 409/412 → re-read + re-apply intent (writer's job)
  | "duplicate"              // 23505 → replay/409, never retry
  | "fence_lost"             // another owner → never retry, abort
  | "ambiguous"              // read-back first, then classify again
  | "permanent";             // validation, authz → never retry

export async function resolveConflict(err: AppError, ctx: WriteContext): Promise<T> {
  switch (classifyRetry(err)) {
    case "transaction_conflict":
      return retryTx(ctx.run, { attempts: 3, baseMs: 25, jitter: "full" }); // fresh reads inside
    case "version_conflict": {
      const current = await ctx.refetch();                  // NEW state, primary
      return ctx.reapplyIntent(current);                    // intent, not payload
    }
    case "duplicate": {
      const existing = await ctx.readByKey();               // read-back by business key
      if (existing) return replay(existing);
      throw new DomainError("SUBSCRIPTION_EXISTS", { http: 409 });
    }
    case "fence_lost":
      await ctx.abort();
      throw new DomainError("WORK_TAKEN_OVER", { http: 409, code: "FENCE_LOST" });
    case "ambiguous":
      throw new DomainError("OUTCOME_UNKNOWN", { http: 202, retryable: true });
    case "permanent":
      throw err;
  }
}
```

```sql
-- Structural prevention for a wallet: constraints do the arithmetic correctly.
ALTER TABLE wallets ADD CHECK (balance_cents >= 0);

UPDATE wallets
   SET balance_cents = balance_cents - $2,          -- atomic; no read-modify-write in app
       version = version + 1
 WHERE id = $1
   AND balance_cents >= $2                          -- precondition == the business rule
RETURNING balance_cents;                            -- 0 rows ⇒ insufficient funds (409)
```

```text
Reconciliation (the safety net):
  nightly: SELECT t.id FROM tenants t
           LEFT JOIN (SELECT tenant_id, count(*) c FROM subscriptions
                       WHERE status='active' GROUP BY 1) s ON s.tenant_id = t.id
           WHERE coalesce(s.c,0) <> t.active_seat_count;
  → any row found = drift that every layer above failed to prevent ⇒ alert + repair job
```

## Key data / numbers

- Retryable under concurrency: **`40001`**, **`40P01`**, MySQL **`1213`**, `55P03` (with your own
  `lock_timeout`) — **whole transaction**, 3 attempts, base 25–50 ms, full jitter.
- Not transport-retryable: **`409`**, **`412`**, **`23505`**, **`422`**, `FENCE_LOST`.
- Ambiguous: **`202 Accepted`** + `OUTCOME_UNKNOWN` while read-back runs.
- Constraint classes that prevent corruption: SQLSTATE **`23505`** unique, **`23514`** check
  violation, **`23503`** FK, **`23502`** not-null.
- Reconciliation cadence: continuous for money (streaming/invariant checks), **daily** for
  relational drift (seat counts, ledger vs balance); tolerance **zero** for balances.
- Conflict metrics worth tracking: `conflict_total{type,endpoint}`, `retry_total{class}`,
  `fence_lost_total` — a rising `version_conflict` rate usually means a hot row or a stale client.

## Real-world use case — Acme SaaS

Acme's seat quota used application-level checks (`if seats < limit then seats+1`). Under a
"bulk-add 50 seats" admin action racing the billing webhook, three concurrent requests all read
`seats=98/limit=100`, all passed the check, and the tenant ended with **103 seats against a
100-seat contract** — a compliance problem, not just a bug, and no error anywhere. The fix: one
atomic `UPDATE ... SET seats = seats + $n WHERE seats + $n <= limit RETURNING seats` plus
`CHECK (seats <= limit)` in the schema as the last line of defense, `409 SEAT_LIMIT_REACHED` when
`rowCount=0`, and a nightly reconciliation of `invoices.seats` vs `tenants.seats`. Concurrent
over-limit writes became impossible; the reconciliation has reported zero drift in eight months,
and it is the *evidence* that the prevention layers hold.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Reject with `409` | no data loss, client decides | user-visible friction | human edits, whole-object writes |
| Re-apply intent automatically | seamless, correct for commutative ops | only valid for commutative ops | counters, quotas, append |
| Field merge | concurrent editors coexist | needs ownership map per field | multi-writer documents/settings |
| LWW | trivial | silent data loss | disposable/telemetry data only |
| DB constraints as arbiter | cannot be raced | errors must be translated well | always — as the final layer |
| Reconciliation only | no protocol changes | data is wrong until it runs | never as the *only* guard for money |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the resolution strategy per conflict type | Let the second `UPDATE` win by accident |
| Retry only classified-transient errors | Retry `409`/`23505` at the transport layer |
| Re-read state inside every retry | Reuse values captured before the conflict |
| Put invariants in `CHECK` constraints | Trust an application `if` for money |
| Run reconciliation and alert on drift | Assume the prevention layers never leak |
| Keep one owner of retry decisions | Retry in repository *and* service |

## Common mistakes

- **Resolving conflicts with a timestamp** — clock skew silently prefers the wrong writer.
- **Auto-merging by overwriting only non-null fields** — you cannot tell "not provided" from
  "cleared," so data disappears.
- **Retrying a conflict with the same `version`** — guaranteed `maxAttempts` failures.
- **No metric for resolutions** — you cannot fix a conflict rate you never observe.
- **Compensating on `fence_lost`** — another worker owns the state now; your undo corrupts *their*
  work.
- **Constraints added later as "cleanup"** — they are the cheapest correctness layer; add them
  with the table.

## Checklist

- [ ] Each conflict type has a named resolution strategy (reject/merge/re-apply/domain rule).
- [ ] Retry classes are explicit; `409`/`412`/`23505`/fence-lost are excluded from transport retries.
- [ ] Retries re-read all state and re-apply intent.
- [ ] Critical invariants have DB constraints, not just application checks.
- [ ] Exactly one layer owns retries per operation.
- [ ] Reconciliation jobs exist for money-adjacent invariants and alert on any drift.
- [ ] Conflict/resolution/retry metrics are on a dashboard.

## Related

- [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](./01-races-optimistic-control-and-version-conflicts.md)
- [Optimistic Concurrency vs Deadlock — deep dive](../02-deep-dive/01-optimistic-concurrency-vs-deadlock.md)
- [Optimistic Locking with a Version Column](../03-practical-examples/01-optimistic-locking-with-version-column.md)
- [Retry Policies (Ch. 27)](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
