# Structural Patterns: Global Handler, Adapter, Boundary, Compensation

> Part XVII · Chapter 46 · Sections 46.1, 46.2, 46.9, 46.10 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 45 — The Four Zones](../../45-organizing-error-handling-modules/01-concepts/03-core-zones-primitives-domain-infra-transport.md)

## In one sentence

Four **structural patterns** decide *where* error handling lives: the **global handler** as the
last-resort boundary, the **error adapter** at every foreign dependency, the **error boundary**
around each unit of user-visible work, and **compensation** inside each multi-step saga.

## Why this matters in production

Structure is what makes the rest of the catalog possible: a retry policy has nothing to attach
to without a boundary; a registry has no consumer without the global handler; translation has
no home without the adapter. When these four are missing, teams compensate with scattered
`try/catch` — and every scattered catch is an unowned fallback decision. Incidents then differ
per endpoint: `/a` returns HTML 500s, `/b` returns empty 200s, the worker hangs. Consistency
starts here.

## Pattern 46.1 — Global handler

**What:** One catch-all at each process/transport edge (HTTP middleware chain end, job runner
wrapper, CLI top level) that receives any error escaping local handling and produces the final
external outcome.

**Solves:** Unknown/unexpected errors have exactly one defined exit: sanitized 500 envelope, DLQ
publish, process exit code. No error path is undefined.

**Must not:** Make business decisions (choosing 402 vs 409), re-translate vendor errors, or
"recover" by returning success. It reads `code`/`category`/registry metadata only.

```ts
// transports/http/error-handler.ts — the last-resort boundary, once per app.
export function globalErrorHandler(err: unknown, req: Request, res: Response, _next: Next) {
  const e = toAppError(err);                    // unknown → INTERNAL_UNEXPECTED
  const entry = REGISTRY[e.code];
  res.status(entry?.httpStatus ?? 500).json(toProblemDetails(e, req));
  // log once, with correlation id; never echo stacks or vendor payloads
}
```

## Pattern 46.2 — Error adapter

**What:** One function per foreign dependency that converts vendor error shapes into the app's
error model, preserving the original as `cause`.

**Solves:** Vendor churn is contained in one file (SDK renames cost one diff); the rest of the
codebase catches only typed app errors; classification becomes testable with fixture errors.

**Must not:** Retry, serialize, or decide business outcomes. Translate only.

```ts
// infra/stripe/errors.ts — adapter for one vendor, one public function.
export function fromStripeError(err: unknown): AppError {
  if (isStripeCardError(err)) return new CardDeclinedError(err.code, { cause: err });
  if (isStripeRateLimit(err)) return new DependencyError("DEP_STRIPE_RATE_LIMITED",
    { retryable: true, cause: err });
  return new DependencyError("DEP_STRIPE_UNAVAILABLE", { retryable: true, cause: err });
}
```

## Pattern 46.9 — Error boundary

**What:** A deliberate containment line — per feature, per request, per job, per UI subtree —
where errors are caught because the fallback there differs from propagation.

**Solves:** Blast-radius control: one optional feature failing degrades that feature, not the
page/request/queue. This is the pattern that turns outages into degradations.

**Must not:** Be drawn at every line. A boundary exists only where a *different outcome*
(degrade, placeholder, partial) is chosen; otherwise propagate.

```ts
// Dashboard: summary card is optional; its failure must not 500 the page.
let summary: Summary | null = null;
try {
  summary = await agentService.summarize(projectId);   // AgentRun path
} catch (err) {
  boundaryLog.warn({ err, projectId }, "summary degraded");
  // fallback: null → UI shows placeholder; page still 200s
}
```

## Pattern 46.10 — Compensation

**What:** In multi-step workflows (sagas), each completed step registers an action that logically
undoes it; when a later step fails, compensations run in reverse order instead of a distributed
rollback.

**Solves:** Cross-store workflows (Checkout: reserve inventory → charge card → activate
subscription) where no single transaction spans the stores. Failure of step N leaves the system
consistent via steps N−1…1's compensations.

**Must not:** Replace local ACID within a single store; compensate steps that were never
confirmed complete; swallow compensation failures (a failed refund must surface to the saga log,
not vanish).

```ts
// workflows/checkout-saga/saga.ts — steps and their compensations, colocated.
const hold = await inventory.reserve(cart);            // step 1
try {
  const charge = await payments.charge(card, total);   // step 2
  try {
    await subscriptions.activate(tenantId, plan);      // step 3
  } catch (err) {
    await payments.refund(charge);                     // compensate 2
    throw err;
  }
} catch (err) {
  await inventory.release(hold);                       // compensate 1
  throw err;
}
```

## Key data

- **Global handler count:** exactly **1 per transport** (HTTP, job runner, webhook ingest, CLI).
  Two HTTP error handlers in one app is itself a defect signal.
- **Adapter count:** exactly **1 public translation function per vendor**; adding a vendor adds
  one folder, zero handler changes.
- **Boundary placement at Acme:** feature-level optional calls (LLM summary, recommendations),
  request-level (HTTP middleware), job-level (`runJob` wrapper), saga-step-level (above).
  ~14 active boundaries for ~40 endpoints — not 40+.
- **Compensation failure contract:** surfaced as `COMPENSATION_FAILED` with the original step
  code; paged, never silently logged. Checkout's refund-compensation success rate target:
  100% within one retry; anything else is an incident.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` originally had no global handler on the webhook transport: each route
handler returned 200 unless its own `try/catch` fired. A malformed `invoice.payment_failed`
payload threw outside the local catch; the framework's default returned an HTML 500; Stripe
treated the whole delivery as retryable and re-sent the *entire* batch for hours, duplicating
processed events (the ingest had partial idempotency). The fix applied three patterns at once:
an error boundary per route (catch → classify), a webhook-transport global handler, and the ack
mapper (permanent signature failures → 400 so Stripe stops retrying; transient → 503 with backoff).
Duplicate-processing volume during the next malformed-payload incident: hours → one batch.

## Trade-offs

| Pattern | Buys | Costs | Misuse |
| ------- | ---- | ----- | ------ |
| Global handler | Defined exit for unknown errors | Can mask missing local handling if relied on exclusively | Doing business routing in the handler |
| Error adapter | Vendor isolation, testable translation | One file per vendor to maintain | Growing into retry/serialization duties |
| Error boundary | Degradation, blast-radius control | Boundaries everywhere → masking noise | Boundary at every line |
| Compensation | Cross-store consistency without 2PC | Orchestration complexity; eventual consistency | Compensating local single-store failures |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep one global handler per transport | Add per-route "safety" catch-alls |
| Translate vendor errors in exactly one adapter | `catch (e) { if (e instanceof StripeError)` scattered in services |
| Draw boundaries where fallback differs | Wrap every call in try/catch |
| Log compensation failures as incidents | `catch` a failed refund and continue |

## Common mistakes

- **Global handler as dumping ground.** Feature-specific routing ("if code starts with
  CHECKOUT_ …") migrates into the handler; it becomes the god module of behavior. Keep it
  metadata-driven only.
- **Boundary without fallback.** Catching and re-throwing the same error at every layer is not
  a boundary; it is 46.19 (deep wrappers).
- **Compensation as rollback.** A refund is not a database rollback: money moved. Treat every
  compensation as a new operation with its own failure modes (Chapter 39).

## Checklist

- [ ] Each transport has exactly one global handler; it makes no business decisions.
- [ ] Each vendor SDK is imported only by its adapter.
- [ ] Every boundary has a documented fallback (including "propagate" is not a fallback).
- [ ] Every saga step has a named compensation with a tested failure path.

## Related

- [Modeling Patterns: Result Type, Registry, Translation](./02-modeling-patterns.md)
- [Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
