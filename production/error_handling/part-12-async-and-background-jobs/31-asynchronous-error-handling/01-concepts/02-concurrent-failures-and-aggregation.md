# Concurrent Failures and Aggregation

> Part XII · Chapter 31 · Sections 31.4–31.7 · _Estimated reading time: 18 min_
> **Prerequisite:** [Sync vs Async Error Semantics](./01-sync-vs-async-error-semantics.md)

## In one sentence

When you launch work in parallel, **you must decide before the first failure** whether one rejection
cancels the whole operation (fail-fast) or whether you keep the successes and report the failures
(collect-all) — and that decision is a **product decision**, not a language default.

## Why this matters in production

Parallel fan-out is where partial failure becomes invisible. A dashboard loads five widgets with
`Promise.all`; one widget's dependency times out; the entire dashboard returns `500` even though
four widgets were ready. Or the opposite: an export uses `allSettled` and silently writes a file
missing a tenant's rows. Both are aggregation bugs. The first sacrifices availability; the second
sacrifices correctness.

## The four aggregation primitives

| Primitive | Settles when | On failure | Result shape | Use when |
| --------- | ------------ | ---------- | ------------ | -------- |
| `Promise.all` | All fulfill **or first rejects** | Rejects immediately with first reason | `T[]` | Every result is required |
| `Promise.allSettled` | All settle | Never rejects | `{status, value/reason}[]` | Partial results are useful |
| `Promise.any` | First fulfills **or all reject** | Rejects with `AggregateError` | `T` | Any one source is enough |
| Bounded pool / `for await` | Controlled concurrency | Depends on your loop | Depends | Resource limits matter |

> The same shapes exist across languages: Python `asyncio.gather(..., return_exceptions=True)`,
> Go `errgroup.Group` (fail-fast) vs a results channel (collect-all), Kotlin `coroutineScope`
> (fail-fast) vs `supervisorScope` (collect-all).

## 31.4 — Concurrent failures

Concurrency introduces failure modes that do not exist sequentially:

- **Failure races.** Two branches fail; which error wins depends on timing. `Promise.all` keeps the
  first rejection and *discards the others*, so the error you see may not be the most important one.
- **Orphaned work.** After `Promise.all` rejects, the remaining promises keep running. Their
  rejections are now unhandled unless each has a handler.
- **Resource amplification.** Launching 10 000 promises at once can exhaust sockets and memory,
  turning a slow dependency into a process-wide failure.

```ts
// The loser's rejection becomes unhandled after Promise.all rejects.
await Promise.all([chargeA(), chargeB()]); // chargeB rejects later, unowned
```

```ts
// Attach a handler to every branch so losers are never orphaned.
const results = await Promise.allSettled([chargeA(), chargeB()]);
```

## 31.5 — Aggregating parallel errors

A good aggregate error answers three questions: **what failed, what succeeded, and is the operation
retryable as a whole?**

```ts
type BranchResult<T> =
  | { ok: true; value: T }
  | { ok: false; source: string; code: string; cause: unknown };

async function fanOut<T>(
  branches: Array<{ source: string; run: () => Promise<T> }>,
): Promise<{ values: T[]; failures: BranchResult<T>[] }> {
  const settled = await Promise.allSettled(branches.map((b) => b.run()));
  const values: T[] = [];
  const failures: BranchResult<T>[] = [];

  settled.forEach((r, i) => {
    const { source } = branches[i];
    if (r.status === "fulfilled") values.push(r.value);
    else failures.push({ ok: false, source, code: classify(r.reason), cause: r.reason });
  });

  return { values, failures };
}
```

`AggregateError` (JavaScript, Python 3.11 `ExceptionGroup`) bundles multiple failures for logging
and API responses:

```ts
if (failures.length > 0) {
  throw new AggregateError(
    failures.map((f) => f.cause),
    `${failures.length} of ${branches.length} branches failed`,
  );
}
```

> ⚠️ **Hazard.** An `AggregateError` message is not a contract. Surface **stable codes** per branch
> in your API (`widget: "billing_unavailable"`), not a concatenated English string.

## 31.6 — Fail-fast vs collect-all

This is the decision table to keep on the wall:

| Question | Fail-fast | Collect-all |
| -------- | --------- | ----------- |
| Can the operation be correct with some results missing? | No | Yes |
| Is the work expensive / side-effecting? | Maybe cancel the rest | Let all finish |
| Does the user need per-item feedback? | No | Yes |
| Is a partial result dangerous? | Yes → fail-fast | No |
| Example | Payment capture + ledger write | Dashboard widgets, bulk validation |

**Fail-fast is about safety. Collect-all is about usefulness.** A `Checkout` that partially captures
two of three line items is corrupt, so it fails fast and compensates. An `AgentRun` that fetches
three of four tool results can still answer, so it collects and marks the missing one.

### Fail-fast does not mean "abandon the rest"

```ts
const controller = new AbortController();
try {
  await Promise.all(tasks.map((t) => t.run({ signal: controller.signal })));
} catch (err) {
  controller.abort(); // stop the still-running siblings
  throw err;
}
```

Without the abort, fail-fast leaks work and cost.

## 31.7 — Partial success

Partial success must be a **first-class result**, not an exception with a footnote. If your API can
return "3 of 5 exports ready," model it:

```json
{
  "status": "partial",
  "succeeded": ["orders", "invoices", "users"],
  "failed": [
    { "source": "events", "code": "EXPORT_SOURCE_TIMEOUT", "retryable": true },
    { "source": "audit", "code": "EXPORT_SOURCE_FORBIDDEN", "retryable": false }
  ]
}
```

Rules for partial success:

1. **Never return `200 OK` pretending everything worked.** Use `207 Multi-Status`, a `status`
   field, or a documented `partial` shape.
2. **Separate retryable from terminal failures** so the client knows what to retry.
3. **Persist the successes** before reporting, or a retry will redo them (Chapter 28).
4. **Make the aggregate outcome deterministic**: same inputs, same failure classification.

## Worked example — Acme dashboard widgets

Acme's dashboard loads six widgets. Three are optional (activity, recommendations, usage chart),
three are required (account, invoices, quota). Using `Promise.all` for everything makes one flaky
optional widget blank the page.

```ts
const required = await Promise.all([account(), invoices(), quota()]); // fail-fast
const optional = await Promise.allSettled([activity(), recommendations(), usage()]);

const optionalFailures = optional
  .map((r, i) => (r.status === "rejected" ? { widget: NAMES[i], code: classify(r.reason) } : null))
  .filter(Boolean);

return { ...required, degradedWidgets: optionalFailures };
```

The page renders with `degradedWidgets` shown as placeholders. **Blast radius** shrinks from "whole
dashboard down" to "three cards unavailable."

## Key data / numbers

- `Promise.all` rejects on the **first** rejection; later rejections are not surfaced by it.
- `Promise.allSettled` never rejects; it always returns one entry per input, in input order.
- `Promise.any` rejects only when **all** inputs reject, with an `AggregateError.errors` array.
- Python `asyncio.gather(return_exceptions=True)` returns exception objects in the result list;
  without it, the first exception propagates and other tasks keep running.
- Unbounded `Promise.all` over 10k+ items commonly causes socket/`EMFILE` exhaustion; use a pool
  of ~10–50 concurrent tasks for network fan-out.

## Real-world use case — Checkout

Checkout validates tax, inventory, and fraud in parallel. Inventory and tax are **required**; fraud
scoring is **optional** (fall back to manual review). The team used `Promise.allSettled` for all
three and treated a fraud timeout as success, shipping orders without a score. The fix: fail-fast for
required branches, collect-all only for fraud, and a `fraud_pending` state that blocks fulfillment
until review. Partial success is allowed, but only where the business says it is.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| `Promise.all` | Simple, fast failure | Abandons siblings, hides other errors | All results required, no side effects |
| `Promise.allSettled` | Preserves every outcome | Caller must interpret statuses | Optional branches, bulk ops |
| `Promise.any` | Lowest latency | Hides partial failures | Redundant sources |
| Bounded pool | Protects resources | More code | High-volume fan-out |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide fail-fast vs collect-all per operation | Use one primitive everywhere by habit |
| Abort siblings when failing fast | Let abandoned work keep running |
| Return per-item failure codes | Throw one generic "some items failed" |
| Persist successes before reporting partial | Re-run the whole batch on retry |
| Bound concurrency for network fan-out | `Promise.all` over 10k rows |

## Common mistakes

- **Using `Promise.all` for optional work** — one failure takes down a page that could degrade.
- **Using `allSettled` for required work** — the code proceeds with missing data.
- **Ignoring rejected entries** — filtering `status === "fulfilled"` without logging the rest.
- **Not aborting on fail-fast** — costs continue after the user sees an error.
- **Returning `200` with a partial body** — clients cache it as success.

## Checklist

- [ ] Is each fan-out classified as fail-fast or collect-all, with a one-line reason?
- [ ] On fail-fast, are siblings cancelled?
- [ ] Does every branch have a handler so no rejection is orphaned?
- [ ] Is partial success representable in the API contract?
- [ ] Are retryable and terminal failures distinguished per item?
- [ ] Is concurrency bounded for network/DB fan-out?

## Related

- [Promise.all vs allSettled — Mechanics](../02-deep-dive/01-promise-all-vs-allsettled.md)
- [Partial Success Aggregation Example](../03-practical-examples/01-partial-success-aggregation.md)
- [Chapter 32 — Partial Completion and Failure Contracts](../../32-background-jobs-queues-and-scheduled-tasks/01-concepts/05-partial-completion-and-failure-contracts.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
