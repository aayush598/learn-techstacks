# Workflow Recovery and Long-Running Operations (39.9–39.12)

> Part XV · Chapter 39 · Sections 39.9–39.12 · _Estimated reading time: 22 min_
> **Prerequisite:** [Distributed Transactions, Sagas, and Compensation (39.6–39.8)](./03-distributed-transactions-sagas-and-compensation.md)

## In one sentence

A workflow is **recoverable** only if its state lives outside the process, its **ambiguous
completions can be resolved by reading**, and its progress is recorded as **checkpoints** that a
fresh process can pick up without repeating completed work.

## Why this matters in production

`ExportJob` runs for 40 minutes. The node gets evicted at minute 37. If progress lived in a local
variable, the customer waits 40 more minutes and gets a duplicate file. Long-running operations
also break the request/response reflex: the client's connection is gone long before the work ends,
so the only honest answer to "did it work?" is a **queryable state**, not a return value. Recovery
is not a nicety here — for workflows measured in hours, "restart from zero" is a functional
outage.

## Core concept

### 39.9 Workflow recovery

Recovery has exactly three ingredients:

```text
┌──────────────────────────────────────────────────────────────┐
│ 1. DURABLE STATE     workflow + per-step rows in a database  │
│ 2. RESUMER           code that loads state on boot / on tick │
│ 3. SAFE STEPS        every step idempotent or checkpointed   │
└──────────────────────────────────────────────────────────────┘
```

Recovery strategies, from cheapest to most robust:

| Strategy | Mechanism | Weakness |
|----------|-----------|----------|
| **Re-run whole workflow** | new attempt from step 1 | requires full idempotency of every step |
| **Resume from last step** | skip `done` steps | needs durable per-step state |
| **Resume from checkpoint inside a step** | re-enter a long step mid-way | the step must be chunked (rows, pages) |
| **Reconcile by external truth** | ask Stripe/S3 "what actually happened?" | depends on provider query capability |
| **Operator-driven repair** | human decides from the ledger | slow, but correct for `blocked` states |

### 39.10 Long-running semantics

Long-running changes the contract, not just the timeout:

- **Synchronous response stops meaning "done."** Return `202 Accepted` with a `Location` /
  workflow id, or a resource the client polls. A `200` after 40 minutes is a broken promise.
- **Timeouts become deadlines for segments**, not for the whole workflow. Each step gets its own
  timeout; the workflow gets a total budget (e.g. 24 h) after which it is `expired`, not `failed`.
- **Progress must be reportable.** `percent`, `processed/total`, `current_step` come from the
  ledger — never from an in-memory counter.
- **Cancellation is a state transition**, not a `throw`. The workflow moves to `cancelling`, stops
  admitting new steps, runs compensations for done steps, then reaches `cancelled`.

### 39.11 Ambiguous completion

When a step's caller cannot tell whether it finished, the workflow has an **unknown** step. Resolve
it in a fixed order:

```text
1. READ-BACK  → does an idempotent marker exist?      yes → done
2. PROVIDER Q → can Stripe/S3/list tell me?           found → done
3. WAIT+READ  → give the system time to settle, re-read (bounded, e.g. 3 tries / 30 s)
4. ESCALATE   → mark step 'unknown', workflow 'needs_review'; NEVER guess
```

The two wrong answers are symmetric and both expensive: guessing **failed** double-charges on
retry; guessing **succeeded** grants entitlements that never paid.

### 39.12 Resuming interrupted work

Resume safety is a property of *steps*, enforced by three tools:

| Tool | What it guarantees | Example |
|------|--------------------|---------|
| **Idempotency key** | re-running a step is a no-op the second time | `charge:<order_id>` |
| **Checkpoint** | a long step re-enters at the last durable boundary | `ExportJob` writes `last_row_offset` every 1,000 rows |
| **Fencing / lease** | a *stale* worker cannot keep writing after another took over | see Ch. 40 — fencing token |

```ts
// Resume on boot: the ledger, not memory, decides what happens next.
export async function resumeAll() {
  const open = await db.any(
    `SELECT id FROM workflows
     WHERE state IN ('running','compensating','cancelling')
       AND (lease_expires_at IS NULL OR lease_expires_at < now())`);
  for (const wf of open) await claimAndAdvance(wf.id);   // claim = acquire lease
}

async function advance(id: string) {
  const wf = await loadWorkflow(id);
  for (const step of wf.stepsInOrder()) {
    if (step.state === "done" || step.state === "compensated") continue;  // skip
    if (step.state === "pending" || step.state === "running" || step.state === "unknown") {
      await resolveOrRun(wf, step);      // resolve 'unknown' first, then run
    }
    if (step.state === "failed") return compensateOrEscalate(wf, step);
  }
  await finish(wf);                       // exactly one terminal transition
}
```

⚠️ **Hazard.** Resuming without a **lease or fencing token** means the old worker and the new one
run the same step concurrently after a GC pause or network split. Resume must first *claim* the
workflow exclusively (see [40.10–40.11](../../../40-consistency-and-concurrency-failures/README.md)).

## Worked example

```text
ExportJob — checkpointed, resumable, honest about ambiguity

Step ledger for workflow wf_7c1:
  step                 state       checkpoint
  load_scope           done        row_count=48211
  export_rows          running     last_offset=31000      ← crash here (OOM kill, exit 137)
  upload_object        pending     -
  notify               pending     -

On restart (new pod):
  resumeAll() → claim wf_7c1 (lease) → export_rows state='running', last_offset=31000
  → re-open reader at 31000, append with deterministic key s3://exports/wf_7c1.csv
  → completes, then upload_object, notify → state='succeeded'
  Result: no duplicate file, no 40-minute re-run, no customer-visible gap.
```

```python
def checkpoint_every_1000(rows, wf_id, offset):
    out = []
    for i, row in enumerate(rows, start=offset):
        out.append(transform(row))
        if (i + 1) % 1000 == 0:
            with transaction():                       # write data + checkpoint atomically
                write_chunk(wf_id, out)
                update_workflow(wf_id, last_offset=i + 1)
            out = []
    return out
```

## Key data / numbers

- **`202 Accepted`** is the correct response for a workflow started but not finished; pair it with
  a `Location` header or a workflow id for polling.
- Kubernetes sends **`SIGTERM`**, waits **`terminationGracePeriodSeconds` (default 30 s)**, then
  **`SIGKILL`**. A workflow that cannot checkpoint within ~30 s *will* lose in-memory progress on
  every deploy — design checkpoints accordingly.
- Ambiguous-resolution retries: **3 reads over ~30 s** is a common starting point; beyond that,
  escalate rather than loop.
- Lease/visibility timeouts in queues are commonly **30–300 s**; a lease must be **longer than the
  longest step** or you get duplicate runners, and **shorter than your recovery SLA** or resume is
  slow. Start at 5× p99 step duration.
- Workflows need a **budget**: define `expires_at` (commonly 24 h for user-visible workflows, 7 d
  for data pipelines) and a sweeper that moves expired workflows to a terminal state.

## Real-world use case — Acme SaaS

`ExportJob` stored `last_offset` in memory and relied on the queue's redelivery. A redelivery after
a crash restarted at row 0, and because the S3 object key included a timestamp, produced a *second
file* — customers received two exports with different content. The fix: deterministic object key
(`exports/<job_id>.csv`), a durable `last_offset` checkpoint committed with every chunk, a lease so
only one runner owns the job, and `202 + status endpoint` instead of a long-held HTTP connection.
p95 completion time was unchanged, but **duplicate exports fell from ~1.2% of jobs to 0**, and
mid-run deploys stopped restarting jobs from scratch.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Poll a workflow resource | survives disconnects, simple | latency, polling load | long-running, user-visible |
| Hold the HTTP connection | no polling | client/proxy timeouts kill it, outcome ambiguous | only if < ~30 s end-to-end |
| Webhook/callback on completion | push, no polling | needs callback auth + retry logic | server-to-server integrations |
| Re-run from scratch on resume | trivial implementation | wasted work, needs total idempotency | short, cheap steps |
| Checkpointed resume | fast, no duplicates | chunking discipline required | long steps (exports, imports, scans) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Persist step state in the same store as the business data | Keep workflow progress in process memory |
| Return `202` + a queryable id | Block a request for minutes or hours |
| Resolve `unknown` by read-back before acting | Guess failed or succeeded on timeout |
| Claim a workflow with a lease before resuming | Let two runners advance the same workflow |
| Give every workflow an expiry and a sweeper | Let `running` rows live forever |

## Common mistakes

- **Checkpoint written after the data, in a separate transaction** — a crash between the two
  re-does or skips a chunk. Write data + checkpoint in one transaction.
- **Poll endpoint that only returns `running`** — no step, no progress, no way to distinguish
  working from stuck.
- **Cancelling by throwing** — leaves steps half-done; cancellation must be a state machine that
  compensates.
- **No lease** — the queue's redelivery plus your own sweeper run the same workflow twice.
- **Treating `expires` as `failed`** — an expired workflow may have partial effects; it still needs
  compensation, not just a status flip.

## Checklist

- [ ] Every long workflow has durable per-step state and a resumer.
- [ ] Clients get `202` + id; progress is queryable with step and percentage.
- [ ] Ambiguous steps have a documented read-back resolution path.
- [ ] Resume acquires a lease/fencing token first.
- [ ] Long steps are chunked with atomic data+checkpoint writes.
- [ ] Workflows expire, and expiry runs compensation.
- [ ] The checkpoint interval fits inside a `SIGTERM` grace period.

## Related

- [States, Compensation Safety, and Irreversibility (39.13–39.16)](./05-states-compensation-safety-and-irreversibility.md)
- [Checkpointing and Idempotent Resume](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/02-deep-dive/03-checkpointing-and-idempotent-resume.md)
- [Distributed Locks, Leases, and Fencing (40.10–40.11)](../40-consistency-and-concurrency-failures/01-concepts/04-distributed-locks-fencing-and-replicas.md)
- [Cancellation, Timeouts, and Events](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/01-concepts/03-cancellation-timeouts-and-events.md)
