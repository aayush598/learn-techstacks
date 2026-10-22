# Double Handling, Handler Failures, Terminal State, and the Standard Lifecycle

> Part IV · Chapter 11 · Sections 11.14–11.17 · _Estimated reading time: 20 min_
> **Prerequisite:** [Response, Finalization, and Cleanup](./04-response-finalize-and-cleanup.md)

## In one sentence

The last four stages are the lifecycle's **guard rails**: an error is handled **once** (11.14),
the handling machinery itself is treated as **fallible code** (11.15), the outcome reaches a
**terminal state** nothing can reopen (11.16), and the whole sequence is **written down as the
project standard** (11.17).

## Why this matters in production

Perfect stages 1-13 still fail if the guard rails are missing:

- A worker and an HTTP client both retry the same failure -> **duplicate side effects** — the
  lifecycle's most expensive bug.
- The error serializer throws on a circular `cause` -> the safety net catches the *serializer's*
  error and the original failure vanishes from the response entirely.
- A job "fails" but the row remains retryable -> a replay six weeks later re-executes a stale
  operation against new state.
- Each new engineer invents their own mini-lifecycle -> the same failure has four behaviors.

Guard rails turn a correct-by-inspection design into a correct-by-default codebase.

## Stage 14a — Preventing double handling (11.14)

**Handle-once is a lifecycle invariant, not a style preference.** Two levels:

1. **Cross-layer (Chapter 9):** one layer decides per code — enforced by the handle-once ledger.
2. **Cross-entry-point (this stage):** the same logical operation triggered via HTTP, queue, and
   cron must converge on **one** decision path — the application service — and the *duplicate
   trigger itself* must be collapsed by idempotency keys (Chapter 28) or job keys.

Mechanisms that make handle-once observable:

```text
· attempt marker on the error object:  e.handled = true   (set by the decider)
· single-writer assertion in tests:    exactly one side effect per fault injection
· response-writer guard:               headersSent check (Ch. 10)
· ledger:                              code -> one handling layer (Ch. 9 reference)
```

The `handled` marker is a cheap runtime net: filters and workers check it and refuse to
re-decide. Treat a second decision attempt as a bug, not a fallback.

## Stage 14b — Failures during error handling (11.15)

The handler is code: it can throw, hang, and write twice. The lifecycle requires a **nested
safety design**, not trust:

| Handler component | Failure mode | Defense |
| ----------------- | ------------ | ------- |
| serializer (`toProblem`) | circular refs, bad encoding | try/catch -> hard-coded minimal body + correlation ID |
| redaction | pathological input, regex blowups | allowlist-first design; timeouts |
| logger | disk full, sink down | never block the response path on logging |
| compensation step | provider down | retry compensation with its own budget; record `COMPENSATION_FAILED` |
| DLQ write | broker down | capped retry; if still failing, terminate the process (Ch. 9, 9.12) so the message is redelivered |
| retry scheduler | queue/clock issues | fall back to immediate bounded retry or terminal |

The meta-rule: **the fallback for a failing handler must be smaller and more boring than the
handler** — a fixed `{"status":500,"code":"INTERNAL_ERROR"}` body beats a second, smarter
attempt. And the original error must be logged *before* any of this (log-first ordering).

## Stage 14c — Terminal state (11.16)

Terminal means: **no further lifecycle action may change this outcome.** Non-terminal states
(`pending`, `running`, `retry_scheduled`) must have **deadlines** that force movement toward a
terminal state — otherwise "temporarily stuck" is indistinguishable from "lost."

```text
 retry_scheduled --deadline--> failed_retries_exhausted (terminal)
 running         --lease-----> failed (ABANDONED) (terminal)
 compensating    --budget----> compensation_failed (terminal, alerted)
```

Replay of a terminal failure is a **new operation** referencing the old one — never a
resurrection of the old record. That single rule prevents most zombie-job incidents.

## Stage 14d — The standard lifecycle for every project (11.17)

Write this once (Chapter 55 houses the doc; this is the template):

```text
For every operation in this system:
 1. Errors originate at enumerated points (failure inventory).
 2. Detection converts immediately to AppError { code, category, retryable, cause }.
 3. Enrichment adds allowlisted context; cause is never dropped.
 4. Translation happens only at the six boundary points (Ch. 9 T1-T6).
 5. Exactly one layer decides; retries <= 5 with backoff + jitter; compensation is idempotent.
 6. Renderers emit one envelope per protocol; no stacks, no causes, correlation ID included.
 7. Every started operation reaches a terminal record (sweeper backstop for crashes).
 8. Cleanup is structural, bounded, and preserves the primary error.
 9. Handler failures degrade to a fixed minimal body; they never mask the original.
10. Any new entry point (route, job, CLI, webhook) adopts this lifecycle, not a new one.
```

The test of a standard: a new engineer implementing a new endpoint without reading this book
still produces something that matches stages 1-14 because the framework, the registry, and the
lint rules made the right path the easy path (Chapters 53-54).

## Worked example — the same failure, guarded lifecycle

```ts
// decider sets the marker; everyone downstream refuses to re-decide
export function decide(e: AppError, ctx: AttemptCtx): Decision {
  if (e.handled) throw new Error(`decision attempted twice for ${e.code}`);  // guard rail
  e.handled = true;
  if (!e.retryable) return { kind: "abort" };
  if (ctx.attempt >= ctx.max) return { kind: "abort", reason: "retries_exhausted" };
  return { kind: "retry", delayMs: backoff(ctx.attempt) };
}
```

```ts
// serializer is itself defended (stage 14b)
export function safeProblem(e: AppError, reqId: string) {
  try { return toProblem(e, reqId); }
  catch {
    logger.error({ reqId, code: e.code }, "serializer failed; minimal body");
    return { status: 500, code: "INTERNAL_ERROR", "request-id": reqId };
  }
}
```

## Key data / numbers

- Terminal vocabulary (five values, no ad-hoc strings): `succeeded`, `failed`, `compensated`,
  `canceled`, `failed_retries_exhausted` (+ DLQ reference).
- Retry cap recommendation: **5** attempts; unknown errors: **1** retry then DLQ.
- Lease/heartbeat sweeper: expire `running` after **2-3** missed heartbeats to
  `failed(ABANDONED)`.
- A minimal hard-coded fallback body should fit in a log line: `{"status":500,"code":
  "INTERNAL_ERROR","request-id":"<id>"}`.

## Real-world use case — Acme SaaS double replay

Two engineers independently wired `ExportJob` retries: one in the queue consumer, one inside the
application service. Result during a Postgres blip: **9 executions** of the same export (3 x 3),
S3 objects rewritten mid-read by downstream consumers, and duplicate `failed` records with
different codes. The guard-rail fix was three parts: the `e.handled` marker (a second decision
threw in staging, immediately), a fault-injection test asserting exactly one side effect, and
the ledger row naming the worker as the sole decider. A second incident of the same class has
not occurred in 14 months.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Guard-railed lifecycle (marker, sweeper, defended handler) | Correct by default; cheap nets | Slightly more scaffolding | Default for any production system |
| Convention-only discipline | Zero code | Drifts with headcount | Never beyond small teams |
| Trust the handler | Least code | One serializer bug erases failures | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set a `handled` marker at the decider | Let a second layer re-decide "just in case" |
| Defend the serializer/redaction with a fixed fallback | Assume the handler cannot throw |
| Force every non-terminal state to have a deadline/lease | Leave rows `running` with no backstop |
| Make replay a new operation | Reactivate terminal records |

## Common mistakes

- **Guard only at one entry point** — the marker lives in the worker but not the HTTP path;
  the double decision returns via the other door.
- **Fallback that tries to be clever** — a "smart" serializer fallback that itself throws; keep
  it dumb and hard-coded.
- **`pending` without a deadline** — every stuck state needs a sweeper; if you cannot name the
  sweeper, the state is effectively terminal-but-unrecorded.

## Checklist

- [ ] The decider sets `handled`; filters/workers check it.
- [ ] Serializer, redaction, and DLQ writes have boring fallbacks.
- [ ] Every non-terminal state has a lease or deadline that forces finalization.
- [ ] Replay creates a new operation referencing the old.
- [ ] The ten-line standard above exists in your repo and is linked from onboarding.

## Related

- [Response, Finalization, and Cleanup](./04-response-finalize-and-cleanup.md)
- [Preventing Double Handling and Failures During Handling](../02-deep-dive/01-double-handling-and-error-during-handling.md)
- [Finalization, Cleanup, and Terminal States](../02-deep-dive/02-finalization-cleanup-and-terminal-states.md)
- [Chapter 55 — Error-Handling Documentation](../../../part-21-maintainability/55-error-handling-documentation/README.md)
