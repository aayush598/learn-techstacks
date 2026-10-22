# Concurrency, Cancellation, Partial Failures, and Recovery Preconditions (51.13–51.16)

> Part XX · Chapter 51 · Sections 51.13–51.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Chapter 40 — Consistency and Concurrency Failures](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md), [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)

## In one sentence

The last four properties cover what happens when **many things fail at once, some of them are
cancelled, and the recovery itself might be wrong**: error handling must be concurrency-safe,
must report partial results accurately, must never turn cancellation into success, and must check
recovery preconditions before it acts.

## Why this matters in production

- **Concurrency bugs in error handling** (51.13) are the "check-then-act" family: two workers read
  "no record yet", both insert, both charge. The application logic was correct; only the error
  handling (the dedupe check) was not atomic.
- **Inaccurate partial reporting** (51.14) is the batch import that says "failed" for a file where
  9 998 of 10 000 rows imported. Support cannot tell which 2 failed, so the customer re-runs the
  whole import — and duplicates the 9 998 that worked.
- **Cancellation reported as success** (51.15) is the request where the client disconnected after
  the payment was captured. The server says "done" in the logs; the customer says "I closed the
  tab"; the money moved and nobody knows.
- **Recovery without preconditions** (51.16) is the refund issued for a charge that never
  happened, or the retry that fires 2 seconds after the caller's deadline.

## Core concept

### 51.13 — Concurrency-safe

Error-handling code frequently holds shared mutable state:

| Shared state | Typical code | Race |
| ------------ | ------------ | ---- |
| Dedupe cache | `if (!cache.has(k)) { cache.set(k, true); doWork(); }` | Two workers both pass the check |
| Compensation ledger | `compensations.add(id)` in a `Set` | Double compensation |
| Retry counter | Module-level `let attempts = 0` | Cross-request contamination |
| "Last error" | `lastError = err` for a logger | Error from request B reported for request A |
| Error accumulator | `errors.push(e)` on a shared array | Lost errors, mixed requests |

The rule: **error state is per-operation, not per-process.** Per-operation means per-request
context, per-job, per-work-item.

```ts
// ❌ Shared mutable error state, keyed by nothing.
let lastError: unknown;
async function handle(id: string) {
  try { await work(id); }
  catch (err) { lastError = err; }     // now shared by every concurrent call
}

// ✅ Per-operation state, immutable, carried explicitly.
type OpContext = { opId: string; errors: readonly OpError[] };
function addError(ctx: OpContext, e: OpError): OpContext {
  return { ...ctx, errors: [...ctx.errors, e] };   // copy-on-write, no shared mutation
}
```

For the dedupe race, the fix is not a lock — it is a **database constraint** that makes the check
and the act atomic:

```sql
INSERT INTO webhook_events (provider, event_id, payload)
VALUES ($1, $2, $3)
ON CONFLICT (provider, event_id) DO NOTHING
RETURNING id;
-- 0 rows returned ⇒ the event was already processed ⇒ success, not failure.
```

### 51.14 — Partial failures accurate

The property has three parts, and all three must hold:

1. **Completeness**: reported successes + reported failures == attempted items.
2. **Soundness**: every reported success is durable.
3. **Unambiguity**: every reported failure is either not-durable or explicitly compensated.

```ts
type BatchResult<T> =
  | { outcome: "all_succeeded"; items: T[] }
  | { outcome: "partial"; succeeded: number; failed: ItemFailure[]; total: number }
  | { outcome: "all_failed"; failed: ItemFailure[]; total: number };
```

The forbidden shape is `outcome: "failed"` with no detail about what *did* work, because it forces
the caller to assume nothing happened.

### 51.15 — Cancellation not success

Cancellation has three distinct moments, and they need three different outcomes:

```text
   cancelled BEFORE the effect      → outcome: cancelled, no effect, safe to retry
   cancelled DURING the effect       → outcome: unknown, effect may exist, do NOT retry blindly
   cancelled AFTER the effect        → outcome: success, effect exists, report success
```

The middle case is the dangerous one. The implementation pattern is a **linearization point**: a
single atomic step after which the operation is committed. Before it, cancellation is free; after
it, cancellation must be reported as success (or the operation is reconciled later).

```ts
async function checkout(ctx: RequestContext) {
  const attempt = await createAttempt();               // pending
  try {
    const charge = await payments.charge(ctx, attempt); // EXTERNAL effect
    await db.query(
      `UPDATE checkout_attempts SET status='charged', charge_id=$2 WHERE id=$1`,
      [attempt.id, charge.id]);                         // ← linearization point
    ctx.signal.throwIfAborted();                        // after this, success is truthful
    return { outcome: "success", attemptId: attempt.id };
  } catch (err) {
    if (ctx.signal.aborted) {
      // 51.15: cancelled is not success, and not automatically retryable.
      const status = await attemptStatus(attempt.id);   // read-back
      return status === "charged"
        ? { outcome: "success", attemptId: attempt.id }
        : { outcome: "cancelled", attemptId: attempt.id };
    }
    throw err;
  }
}
```

### 51.16 — Recovery preconditions

Recovery (retry, compensation, replay, fallback escalation) is a **decision with preconditions**.
If the preconditions do not hold, the correct behaviour is to *stop* and record why.

| Recovery action | Preconditions |
| --------------- | ------------- |
| **Retry** | Classified transient · operation idempotent · deadline not exhausted · budget available · dependency healthy |
| **Compensate** | The original effect is known to have happened · compensation is itself idempotent · a compensating action exists |
| **Replay a job** | Payload schema still valid · job is not already in a terminal state · no newer version superseded it |
| **Escalate to fallback** | The fallback is defined for this category · the fallback returns a *different* result, not the same failure |

```ts
// ✅ Recovery is a decision with an explicit stop reason.
type Recovery = { action: "retry" } | { action: "stop"; reason: string };

function decideRecovery(err: AppError, op: OpState): Recovery {
  if (!err.classification.retryable) return { action: "stop", reason: "permanent_error" };
  if (!op.idempotent)                return { action: "stop", reason: "not_idempotent" };
  if (op.deadlineExpired())           return { action: "stop", reason: "deadline_exhausted" };
  if (!op.budget.available())         return { action: "stop", reason: "retry_budget_exhausted" };
  return { action: "retry" };
}
```

The "stop" reasons are not failure — they are **evidence**. They are what tells the next engineer
why the system did not retry, instead of leaving a silent gap in the logs.

## Worked example — `ExportJob` (Acme SaaS)

`ExportJob` processes **10 000 rows** in batches of 500. Two workers can pick up the same job
after a lease expiry, and customers can cancel exports mid-flight.

```ts
// BEFORE — three properties at once.
async function process(job: ExportJob) {
  for (const batch of chunk(job.rows, 500)) {
    try {
      await writeBatch(batch);
    } catch (err) {
      log.error(err);
      continue;                        // 51.14: failures vanish; batch count lies
    }
  }
  await db.query(`UPDATE export_jobs SET status='done' ...`);  // 51.14: "done" despite failures
}
```

- **51.13**: two workers running the same job both write the same rows (duplicate effects).
- **51.14**: `continue` drops the failure; the job ends as `done` even if 40 batches failed.
- **51.15**: a cancel during `writeBatch` was caught by the same `catch` and treated as a
  recoverable row error, so the job continued to completion after the customer asked to stop.
- **51.16**: the retry used for transient S3 errors had no deadline check and no idempotency
  requirement — a retried batch could append rows twice.

After:

```ts
async function process(job: ExportJob, ctx: OpContext) {
  const results: ItemFailure[] = [];
  let succeeded = 0;

  for (const batch of chunk(job.rows, 500)) {
    if (ctx.signal.aborted) {                 // 51.15: cancellation is checked at a known point
      await finish(job, { outcome: "cancelled", succeeded, failed: results, total: job.rows.length });
      return;
    }
    try {
      await writeBatch(batch, { idempotencyKey: `${job.id}:${batch.index}` });  // 51.13: at-most-once
    } catch (err) {
      const decision = decideRecovery(classify(err), op);   // 51.16: preconditions checked
      if (decision.action === "retry") { /* retry the same batch with the same key */ }
      else {
        results.push({ batch: batch.index, code: classify(err).code });        // 51.14: recorded
        succeeded += batch.rows.length - batch.rows.length;
      }
    }
  }
  // 51.14: successes + failures == attempted, and the outcome reflects reality.
  await finish(job, {
    outcome: results.length === 0 ? "all_succeeded" : "partial",
    succeeded, failed: results, total: job.rows.length,
  });
}
```

The customer-facing report changed from "Export complete" to "Export complete — 9 500 of 10 000
rows exported, 10 batches failed (codes listed)". Support stopped guessing.

## Key data / numbers

- **Concurrent-duplicate test size: N = 10** minimum; 50 for money-moving operations.
- **Batch atomicity**: one transaction per batch (500 rows) is a common compromise; per-row
  savepoints are slower but give exact failure positions.
- **Invariant arithmetic**: `succeeded + failed == attempted` must hold *exactly*, including
  cancelled items (count them as `cancelled`, not as `failed` or `succeeded`).
- **Cancellation check points**: before every irreversible effect, and at least every batch.
- **Lease TTL vs job runtime**: TTL must exceed the longest expected step plus the heartbeat
  interval; otherwise duplicate execution (51.13) is guaranteed, not rare.
- **Fencing tokens**: monotonically increasing per lease acquisition; a stale holder's write is
  rejected by the database (`WHERE version = $expected`).
- **Compensation idempotency window**: match the original effect's window (e.g. 24 h for
  payments).
- **Recovery decision stop-reasons worth recording**: `permanent_error`, `not_idempotent`,
  `deadline_exhausted`, `retry_budget_exhausted`, `no_compensation_available`.

## Real-world use case — Acme SaaS `Checkout`

Acme's `Checkout` was called twice by a user who double-clicked "Pay". The frontend sent the same
`Idempotency-Key`, but the backend's dedupe check was:

```ts
if (!(await redis.get(`idem:${key}`))) {
  await redis.set(`idem:${key}`, "1");   // not atomic with the check
  await stripe.charges.create(...);
}
```

Under concurrency, both requests passed the check and both charges were created. Acme's
refund process then had to handle **two refunds** for one order, which the compensation code
forbade ("only compensate if exactly one charge exists") — so the second refund was manual.

Three properties were involved: **51.13** (the check-then-act race), **51.9** (duplicate side
effect), and **51.16** (compensation preconditions were checked, and the precondition did not
hold, but the code had no way to say "I am stopping" — it just did nothing).

The fix was to move the uniqueness decision into the database — an `idempotency_keys` table with a
unique constraint, inserted in the same transaction that records the order — plus a `stop` reason
for the compensation path so the second refund became an explicit, tracked task instead of a
silent no-op. Duplicate charges went from 3–4 per month to 0, and the compensation table grew from
one row to three, each with a reason.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Pessimistic lock around the operation | Simple, obviously correct | Serializes work; deadlock risk | Short, rare, contended critical sections |
| Optimistic concurrency (version + conditional write) | No waiting; conflicts become errors | Callers must handle conflict | High-contention reads/writes |
| Database uniqueness as the arbiter | Race-free by construction | Needs a schema; conflicts surface as `23505` | Side-effect dedupe, idempotency |
| Distributed lock / lease | Works across processes | Needs fencing tokens; lease expiry causes duplicates | Long jobs needing single execution |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep error state per-operation | Use module-level error accumulators |
| Enforce uniqueness in the database | "Check then act" in application code |
| Count cancelled items separately | Fold cancelled into failed |
| Report successes + failures == attempted | Mark a batch job `done` with silent `continue` |
| Check cancellation before irreversible effects | Only check cancellation at the top of the loop |
| Record a stop reason when recovery is refused | Silently skip recovery |

## Common mistakes

- **Dedupe via cache check without atomicity.** A `GET` then a `SET` is two operations; the gap
  between them is where the duplicate happens.
- **Swallowing cancellation in a broad catch.** `catch (err) { continue; }` catches `AbortError`
  too, so cancellation becomes "one more retry".
- **Reporting `done` when some items failed.** The dashboard says "Export complete" and the CSV is
  missing rows.
- **Compensating without reading the current state.** A second compensation for an already-refunded
  charge creates a second refund.
- **Retrying after the caller's deadline.** The work completes; the response has nowhere to go;
  the client retries and creates a duplicate.

## Checklist

- [ ] No error-handling state is shared across concurrent operations.
- [ ] Every side-effecting operation has an atomic uniqueness mechanism.
- [ ] Batch results report successes, failures, and cancellations separately, and the three sum to
      the attempted count.
- [ ] Every reported success is durable before the report is emitted.
- [ ] Cancellation is checked before every irreversible effect and produces a `cancelled` outcome.
- [ ] Recovery decisions check preconditions and record a stop reason when they decline.
- [ ] Concurrent-duplicate tests exist for money-moving operations.

## Related

- [Safety, Resources, and Side Effects (51.5–51.9)](./02-safety-and-resource-properties.md)
- [Transformation and Contract Properties (51.10–51.12, 51.17–51.18)](./03-transformation-and-contract-properties.md)
- [Chapter 40 — Consistency and Concurrency Failures](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
