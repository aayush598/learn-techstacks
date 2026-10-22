# Finalization, Cleanup, and Terminal States

> Part IV · Chapter 11 · Sections 11.12, 11.13, 11.16 · _Estimated reading time: 19 min_
> **Prerequisite:** [Response, Finalization, and Cleanup](../01-concepts/04-response-finalize-and-cleanup.md)

## In one sentence

**Finalization** writes the durable outcome record, **cleanup** releases everything acquired on
the failure path, and **terminal state** guarantees the outcome can never be silently reopened —
the three stages that make a failure *actually over*.

## Why this matters in production

Failures here are the "ghosts" of production systems:

- A checkout stuck `pending` because the crash happened between "charge succeeded" and "row
  updated" — support cannot refund or retry without guessing.
- An S3 multipart upload never aborted — the tenant pays for weeks of garbage-parts storage.
- A lock or lease held by a dead process — every subsequent run fails with a mysterious
  conflict until someone SSHs in.
- A "failed" job whose record says `retry_scheduled` — a broker replay a month later executes a
  stale operation against new data, corrupting a report.

These are not exotic: they are the ordinary consequence of treating stages 12-13-16 as
afterthoughts.

## Stage 12 — Finalization mechanics (11.12)

Finalization answers: **what durable fact records that this operation is over, and how did it
end?**

Design rules:

1. **One record of record.** A row, a job state, an event — chosen per operation type. Logs are
   not the record.
2. **Idempotent writes.** `markFailed(id, code)` called twice (retry of the finalize itself,
   sweeper racing the worker) must converge to the same terminal value.
3. **Ordering for queues:** where possible, finalize **before** ack, because ack-then-crash
   loses the outcome; where UX demands fast responses (HTTP), finalize must be crash-safe
   (durable write in the same transaction as the state change, or an outbox).
4. **Ambiguous outcomes are first-class.** If the process dies *during* commit, you may not
   know whether the operation succeeded. Record `UNKNOWN`/`ABANDONED` and resolve by
   read-back (Chapter 23's ambiguous outcomes) — never guess `failed` when the charge may have
   gone through.

```ts
// finalize-before-ack, with sweeper backstop
try {
  await runExport(msg);
  await exportsRepo.markSucceeded(msg.jobId);       // durable outcome FIRST
  await queue.ack(msg);
} catch (err) {
  const e = normalize(err);
  await finalizeFailure(msg, e);                    // idempotent terminal write
  await queue.ack(msg);                             // message handled; record carries the truth
}

// sweeper: converts zombies to terminal
async function sweepAbandoned() {
  await exportsRepo.expireStaleRunning(leaseMs: 2 * heartbeatIntervalMs,
                                       toState: "failed", code: "ABANDONED");
}
```

## Stage 13 — Cleanup on the failure path (11.13)

Cleanup releases acquisitions in reverse order, structurally (`finally`/`defer`/context
managers — Chapter 14 owns the primitives). The lifecycle adds three requirements:

| Requirement | Practice |
| ----------- | -------- |
| **Bounded** | each cleanup step gets a timeout; total budget < drain window (~30 s default; keep cleanup ≤ ~5-10 s) |
| **Idempotent** | releasing twice is safe (abort of an already-aborted multipart upload returns a known error — treat as success) |
| **Primary-preserving** | cleanup failure is attached as secondary; the original error still travels |

```ts
const lease = await locks.acquire(jobId, { ttlMs: 30_000 });
try {
  await doWork();
} finally {
  await withTimeout(locks.release(lease), 2_000)          // bounded
    .catch((releaseErr) => log.warn({ releaseErr }, "lease release failed; TTL will expire"));
}
```

⚠️ **Hazard.** TTLs are the backstop for failed releases, not a substitute: a lease that always
expires by TTL means every failure costs a full TTL of stalls for that key.

## Stage 16 — Terminal states and the no-resurrection rule (11.16)

Terminal vocabulary (standardize these five plus a code):

```text
succeeded | failed(code) | compensated(code) | canceled(reason) | failed_retries_exhausted(+dlqRef)
```

Properties enforced by the state machine:

1. **No transitions out of terminal.** `UPDATE ... WHERE id=$1 AND state NOT IN (terminal)`.
   The database (or equivalent) is the enforcement point, not application discipline.
2. **Non-terminal states have expiries.** `pending`, `running`, `retry_scheduled`, `compensating`
   each carry `lease_expires_at`/`deadline_at`; the sweeper converts expiry to a terminal state.
3. **Replay is new-and-referencing.** `replay_of: job_9f21c` creates a *new* record in a fresh
   non-terminal state; the old record stays terminal forever. Auditors and idempotency both
   depend on this.
4. **Compensated is terminal.** A compensated saga is over; re-attempting the business intent is
   a new saga, not a retry.

## The failure-path sequence, end to end

```text
 error decided ABORT
   ├─ stage 11: render 503 + Retry-After (HTTP) or record attempt (job)
   ├─ stage 12: markFailed(id, code) — idempotent, before ack
   ├─ stage 13: rollback tx · release locks · abort multipart · close streams
   ├─ verify:   state IN terminal_states  (assert in tests)
   └─ done:     nothing may reopen this record; replay = new operation
```

## Key data / numbers

- Terminal set (five): `succeeded`, `failed`, `compensated`, `canceled`,
  `failed_retries_exhausted`.
- Sweeper recommendation: heartbeat interval **~10 s**; expire after **2-3** missed heartbeats
  (20-30 s); sweep cadence ≤ the expiry window.
- Cleanup budget: **≤ 5-10 s** total under Kubernetes' **30 s** default grace, leaving room for
  log flush and graceful close.
- Lease TTL: sized to **> max operation duration**, else healthy workers get stolen-from;
  typical long-job TTLs are **30-120 s** with renewals.
- Ambiguous-commit handling: read-back verification before declaring either terminal state
  (Chapter 23).

## Real-world use case — Acme SaaS ambiguous charge

An OOM kill landed between Stripe's `200` and Acme's `markSucceeded`. The record said
`running`; the sweeper marked it `failed(ABANDONED)` after 25 seconds; a human replayed it; the
customer was charged **twice** for one subscription.

Lifecycle fix, three parts: (1) the payment reservation carried the idempotency key, so replay
*read back* Stripe by key before charging (ambiguous-outcome resolution); (2) finalize-wrote the
charge ID *before* the expensive steps continued; (3) the sweeper's `ABANDONED` triggered a
**read-back workflow**, not a blind replay. The double charge class disappeared, and the two
historical cases were refunded from the now-reliable record of record.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Finalize-before-ack + sweeper + no-resurrection (recommended) | No zombies, no stale replays | Sweeper + state machine scaffolding | Default for jobs/sagas |
| Ack-first for latency | Faster queue drain | Lost outcomes on crash | Only for truly disposable events |
| Sweep-only (no explicit finalize) | Simple worker | Terminal data quality depends on heuristics | Never for money |
| Resurrect and retry old records | "No lost work" | Stale execution against new state | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Finalize before ack when possible | Ack, then update the record "later" |
| Enforce no-transitions-out in the DB | Trust application code alone |
| Give every non-terminal state an expiry | Leave `running` unbounded |
| Treat `compensated` as terminal | Retry a compensated saga in place |
| Read back before replaying ambiguous ops | Guess `failed` when the charge may exist |

## Common mistakes

- **Sweeper as the primary path** — if most terminal states come from the sweeper, your
  in-process finalize is broken; alert when sweep rate rises.
- **TTL without renewal** — long exports exceed the lease, another worker takes over, and two
  workers run the same job; renew leases or size TTL generously.
- **Finalize writes that are not idempotent** — `state = 'failed'` unconditional clobbers
  `compensated`; guard transitions.

## Checklist

- [ ] One record of record per operation; finalize writes are idempotent.
- [ ] Terminal states are enforced by the storage layer.
- [ ] Sweepers convert all expirable states to terminal with codes.
- [ ] Cleanup is bounded, idempotent, primary-preserving.
- [ ] Replays create new records referencing the old.
- [ ] Ambiguous outcomes trigger read-back, never blind replay.

## Related

- [Response, Finalization, and Cleanup](../01-concepts/04-response-finalize-and-cleanup.md)
- [Preventing Double Handling and Failures During Handling](./01-double-handling-and-error-during-handling.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
