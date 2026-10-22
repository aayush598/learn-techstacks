# Response, Finalization, and Cleanup

> Part IV · Chapter 11 · Sections 11.11–11.13 · _Estimated reading time: 18 min_
> **Prerequisite:** [Propagation, Translation, and Recovery](./03-propagation-translation-and-recovery.md)

## In one sentence

Stages 11–13 turn a decided error into something the outside world can **see** (the response),
into a record nobody can **un-see** (the terminal outcome), and into a system with **nothing
left held** (cleanup) — in that order, on every path.

## Why this matters in production

These three stages fail quietly:

- **Render-only thinking:** the API returns `503` but the job row stays `pending`; an hour later
  the customer's export "still running" is really a corpse.
- **Finalize-only thinking:** the job is marked `failed` but the transaction is left open, the S3
  multipart upload is left incomplete, and the tenant's lock is held — the *next* run fails with
  confusing `40001`s.
- **Cleanup without finalize:** resources are released, but nobody recorded *why* the operation
  ended; on-call sees freed connections and no failure record.

A lifecycle is only credible if all three stages run — including on the failure path, including
when the process is draining (Ch. 9, 9.12).

## Stage 11 — Converting to external responses (11.11)

Rendering is the *mechanical* translation of the decided outcome to a protocol shape. It belongs
to the entry-point renderer (controller/filter for HTTP, attempt recorder for workers — Chapters
9 and 10), and it never re-decides.

| Decided outcome | HTTP render | Job render |
| --------------- | ----------- | ---------- |
| `ABORT` + permanent code | `4xx` + envelope (`409`, `422`, `402`…) | terminal record, no retry |
| `RETRY` budget left | (no response yet; keep working) | attempt record + delayed retry |
| `RETRY` exhausted | `503`/`429` + `Retry-After` | terminal + DLQ |
| `DEGRADE` | `200` with degraded flag/content | success with flag |
| unclassified | `500` + correlation ID | 1 retry then DLQ |

Rules: one body-writer (Ch. 10 ordering), `headersSent` guard for streams, **no** stack traces,
no cause chains, no vendor objects — code + safe detail + correlation ID only (Chapters 20, 34).

## Stage 12 — Finalizing the failed operation (11.12)

**Finalization** is the durable record that the operation is over and how it ended. The rule:
**every started operation reaches a terminal record.** `pending` is a stage, not a state of
rest.

```text
 started ──▶ running ──▶ succeeded
                     └──▶ failed(code, detail)          terminal
                     └──▶ compensated(code)             terminal (saga undone)
                     └──▶ canceled(reason)              terminal
                     └──▶ failed_retries_exhausted     terminal (+ DLQ ref)
```

Mechanics that make it true: the terminal write is **itself** retried/robust (it is the record
of record); the worker updates the row *before* acking the message where possible; a sweeper
process (or lease expiry) converts abandoned `running` rows to `failed(ABANDONED)` — because
crashes skip in-process finalization by definition (Ch. 9, 9.12).

## Stage 13 — Cleanup after failure (11.13)

Cleanup releases everything acquired on the way: transactions (rollback), locks, temp files,
multipart uploads, streams, in-memory buffers. Three properties:

1. **Structural:** `finally` / `defer` / context managers — cleanup runs on the failure path
   (Chapter 14 owns the mechanics).
2. **Bounded:** cleanup gets its own short timeout; an S3 abort that hangs must not exceed the
   drain window (Kubernetes' 30 s grace, Ch. 9).
3. **Secondary-error-safe:** if cleanup itself fails, the **primary** error stays the one that
   travels; the cleanup failure is attached as secondary/suppressed (Chapter 14's primary-error
   rule).

```ts
const upload = await s3.createMultipartUpload(params);
try {
  await uploadParts(upload, rows);                 // may fail at any point
  await s3.completeMultipartUpload(upload);
} catch (err) {
  try { await s3.abortMultipartUpload(upload); }   // stage 13 — bounded, failure-safe
  catch (abortErr) { log.warn({ abortErr, cause: err }, "abort failed; lifecycle lease will expire"); }
  throw err;                                        // primary preserved
}
```

## The ordering that ties them together

```text
 DECIDE (9) ──▶ APPLY (10) ──▶ RENDER (11) ──▶ FINALIZE (12) ──▶ CLEANUP (13) ──▶ TERMINAL (14)
                    │               │                │                │
                    │               │                │                └─ release resources (always)
                    │               │                └─ durable terminal record (always)
                    │               └─ protocol shape (per entry point)
                    └─ retries/compensations executed (budgeted)
```

Note: for HTTP, render may precede finalize in wall-clock time (respond, then record); the
lifecycle requirement is that **both happen**, and that finalize is robust to the process dying
right after the response. For jobs, finalize typically precedes ack.

## Key data / numbers

- Terminal outcome vocabulary worth standardizing: `succeeded`, `failed`, `compensated`,
  `canceled`, `failed_retries_exhausted` (+ DLQ reference) — five values, no ad-hoc strings.
- `Retry-After` on exhausted-retry responses: seconds; recommend telling the client a realistic
  window (`30–120` s for provider blips).
- Cleanup timeouts: below the drain window — with Kubernetes' default **30 s** grace, keep
  cleanup budgets **≤ ~5–10 s** so logging/flush still fits.
- Abandoned-work sweeper: recommendation — lease/heartbeat per `running` operation; expire to
  `failed(ABANDONED)` after **2–3** missed heartbeats.

## Real-world use case — Acme SaaS `ExportJob`

An export crashed (OOM kill) mid-upload. Without the three stages: the row stayed `running` for
**nine hours** (no sweeper), the S3 multipart upload accrued storage charges for days (no
abort), and support could not distinguish "slow" from "dead" (no terminal record). With stages
11–13: heartbeats expired the lease in ~4 minutes to `failed(ABANDONED, correlationId=...)`,
the abort-on-failure path (and a lifecycle-based cleanup job for orphaned multipart uploads)
closed the storage leak, and the UI showed a real terminal state with a retry button. Customer
"stuck export" tickets dropped to zero.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Render → finalize → cleanup with a sweeper (recommended) | No zombies; auditable; leak-free | Needs lease/sweeper infrastructure | Any durable operation |
| Finalize only on clean exits | Less code | Zombies on crash — the common case | Never |
| Cleanup only on success path | Fast happy path | Resource leaks accelerate incidents | Never |
| Respond-then-record with durable finalize | Good UX + durable truth | Requires idempotent finalize writes | HTTP money paths |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every operation a terminal record | Leave rows `running` indefinitely |
| Abort incomplete uploads/releases in `finally` | Clean up only when someone notices |
| Bound cleanup with its own timeout | Let cleanup outlive the drain window |
| Keep the primary error when cleanup fails | Replace it with the cleanup's error |

## Common mistakes

- **Finalize-after-ack races** — ack the message, crash before the row update → zombie forever;
  finalize (or at least attempt it) before ack, and keep the sweeper as backstop.
- **Cleanup errors becoming the response** — the user sees "abort failed" instead of the real
  `DB_UNAVAILABLE`; preserve the primary (Ch. 14).
- **Terminal strings inventing themselves** — `done`, `error`, `oops` as statuses; constrain to
  the five-value vocabulary and let codes carry nuance.

## Checklist

- [ ] Renderers emit only code + safe detail + correlation ID.
- [ ] Every started operation has a path to a terminal record, including crash paths (sweeper).
- [ ] Cleanup is structural, bounded, and failure-safe.
- [ ] Finalize writes are idempotent and retried.

## Related

- [Propagation, Translation, and Recovery](./03-propagation-translation-and-recovery.md)
- [Terminal State and the Standard Lifecycle](./05-terminal-state-and-standard-lifecycle.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
