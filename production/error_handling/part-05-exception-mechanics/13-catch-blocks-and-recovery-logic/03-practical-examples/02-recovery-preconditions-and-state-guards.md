# Recovery Preconditions and State Guards

> Part V · Chapter 13 · Sections 13.14–13.16 (practical) · _Estimated reading time: 20 min_
> **Prerequisite:** [Recovery Inside Catch](../01-concepts/03-recovery-inside-catch.md)

## In one sentence

Before you recover, **prove it is safe**: check that the operation is idempotent, the resource is
alive, the state is consistent, and the budget allows it — otherwise translate or terminate instead
of recovering.

## Why this matters in production

Recovery that skips its preconditions is how duplicate charges, corrupted rows, and "refunded but
still shipped" incidents happen. The fix is a short, explicit preflight check before any recovery
action. It costs a few lines and prevents the failures that are hardest to unwind.

## Scenario

**Acme SaaS `ExportJob`** writes chunks to S3 and commits an offset after each. On an S3 error it
wants to retry. The naive retry has three hazards: the offset may have already advanced, the
multipart upload may be half-written, and the error may be permanent. Each hazard maps to a
precondition.

```text
per chunk:
  1. put object to S3        (side effect, may partially apply for multipart)
  2. commit offset to DB     (side effect, non-idempotent if not keyed)

on error, before retrying:
  A. is the error transient?            (else: no retry)
  B. did the offset already commit?     (else: retry would re-export or skip)
  C. is the upload resumable/aborted?    (else: corrupted object)
  D. is there budget left?              (else: fail the job)
```

## The preflight pattern

```ts
interface RecoveryPlan {
  safe: boolean;
  reason?: string;
}

function preflight(chunk: Chunk, err: unknown, state: JobState): RecoveryPlan {
  // A. transient?
  if (!isTransient(err)) return { safe: false, reason: "permanent_error" };

  // B. no partial commit?
  if (state.committedOffsets.has(chunk.offset)) {
    return { safe: false, reason: "offset_already_committed" };
  }

  // C. upload left no corrupt object?
  if (state.partialUploads.has(chunk.key)) {
    return { safe: false, reason: "partial_upload_needs_abort" };
  }

  // D. budget?
  if (state.attempts >= MAX_ATTEMPTS || Date.now() > state.deadline) {
    return { safe: false, reason: "retry_budget_exhausted" };
  }

  return { safe: true };
}
```

Then recovery is a two-phase, guarded operation:

```ts
async function exportChunkGuarded(chunk: Chunk, state: JobState) {
  try {
    await putObjectMultipart(chunk);   // resumable, idempotent on key
    await commitOffset(chunk.offset);  // idempotent: upsert keyed by (job, chunk)
  } catch (err) {
    const plan = preflight(chunk, err, state);
    if (!plan.safe) {
      throw new ExportChunkFailed(chunk.index, plan.reason!, { cause: err });
    }

    // C requires cleanup BEFORE retry: abort the half-written upload.
    await abortUpload(chunk.uploadId).catch((abortErr) => {
      // abort failure is secondary; primary remains the putObject error
      throw new ExportChunkFailed(chunk.index, "abort_failed", {
        cause: err, suppressed: abortErr,
      });
    });

    state.attempts++;
    return exportChunkGuarded(chunk, state); // now safe: A–D all satisfied
  }
}
```

Note: the retry is guarded, the abort is idempotent, and the offset commit is an **upsert** keyed
by `(job, chunk)` so re-running it cannot double-count.

## Making state valid before recovering

Three techniques, in order of preference:

| Technique | Guarantees | Cost |
| --------- | ---------- | ---- |
| **Idempotent operation** | Re-run has no extra effect | Design keys correctly |
| **Rollback then retry** | Clean slate | Requires a transaction/savepoint |
| **Reconcile then retry** | Knows true state from an external source | An extra read |

```ts
// Rollback-before-retry for a DB transaction
async function withRetryableTx<T>(fn: (tx: Tx) => Promise<T>): Promise<T> {
  for (let attempt = 1; attempt <= 3; attempt++) {
    const tx = await db.begin();
    try {
      const result = await fn(tx);
      await tx.commit();
      return result;
    } catch (err) {
      await tx.rollback();                 // ← state is clean before the next attempt
      if (!isTransient(err) || attempt === 3) {
        throw new TxFailed({ cause: err, attempts: attempt });
      }
      await sleep(backoff(attempt));
    }
  }
  throw new Error("unreachable");
}
```

## Decide: recover, translate, or terminate

```text
preflight.safe?
  ├── yes
  │     ├── can complete fully?  → recover (retry/fallback)
  │     └── only partially?      → recover what's safe, RETHROW the rest
  └── no
        ├── can classify safely? → translate to a domain result
        └── state unknown?       → terminate (fail-fast, alert), do not write
```

A terminate example — writing to a resource whose state we cannot establish:

```ts
if (!(await canSafelyWrite(jobId))) {
  throw new FatalStateUnknown(
    `refusing to write export ${jobId}: state could not be verified`,
  );
}
```

## Key data / numbers

- **Multipart uploads**: S3 multipart parts must be aborted (`AbortMultipartUpload`) if abandoned,
  or they remain billable and can corrupt a resumed upload.
- **Idempotent offset commit**: key on `(job_id, chunk_index)`; `INSERT … ON CONFLICT DO NOTHING`
  (PostgreSQL) makes the retry a no-op.
- **PostgreSQL `40001`** (serialization failure): rollback the transaction before retrying; the
  retry will otherwise fail deterministically.
- **Retry budget**: max attempts 3–5 plus a wall-clock deadline; both are preconditions.

## Real-world use case — Acme SaaS

Acme's export retried on any S3 error without checking the offset. Because the offset commit had
succeeded before the S3 error was observed (the error was actually a timeout reading the response),
the retry re-exported the chunk and the CSV contained duplicate rows. The fix added precondition B
(offset already committed → do not retry) and made the commit an upsert keyed by
`(job, chunk)`. Duplicate rows disappeared, and the job could be safely re-run from a checkpoint.

## Trade-offs

| Precondition approach | Pros | Cons | When |
| --------------------- | ---- | ---- | ---- |
| Idempotent by design | Cheapest, safest | Needs key design | New code |
| Rollback + retry | Clean state | Transactions only | DB work |
| Reconcile + retry | Handles ambiguity | Extra read | Unknown-outcome remote calls |
| No precondition check | Less code | Corruption risk | ❌ Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check idempotency/liveness/consistency/budget | Retry on hope |
| Make operations idempotent by key | Retry a non-keyed side effect |
| Rollback before re-running | Retry atop dirty state |
| Abort partial uploads before retry | Resume over a corrupt object |
| Terminate when state is unknown | Write to uncertain state |

## Common mistakes

- **Retrying after the side effect already committed** — double effect.
- **Forgetting to abort partial uploads** — billable, corrupting residue.
- **No budget check** — retries outlive the request/job deadline.
- **Recovering in a catch that also mutates shared state** — races under concurrency.

## Checklist

- [ ] Every retry has a preflight that checks transient, idempotency, liveness, budget.
- [ ] Partial side effects are rolled back or aborted before retry.
- [ ] Commits that may repeat are idempotent (upsert/ON CONFLICT).
- [ ] Unknown state → terminate, never write.
- [ ] Partial recovery rethrows; it does not report success.

## Related

- [Recovery Inside Catch](../01-concepts/03-recovery-inside-catch.md)
- [Typed Catch and Recovery Patterns](./01-typed-catch-and-recovery-patterns.md)
- [Idempotency and Duplicate-Operation Safety (Part XI)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Transaction and Rollback Error Handling (Part IX)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
