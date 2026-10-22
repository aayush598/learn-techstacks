# Nested Boundaries

> Part VI · Chapter 15 · Section 15.16 · _Estimated reading time: 20 min_
> **Prerequisite:** [Ownership, Granularity, and Fallback Behavior](../01-concepts/04-ownership-granularity-and-fallback.md)

## In one sentence

Boundaries nest — a function boundary inside a module boundary inside a request boundary — and the
hard part is making each one **add only what it owns**, never swallowing a failure an outer
boundary needs or stealing a decision that belongs outside.

## Why this matters in production

Nested boundaries are where subtle bugs live. An inner `catch` that turns a failed write into a
`null` breaks an outer invariant; an inner `catch` that logs and rethrows duplicates logs; an inner
`catch` that retries swallows the retry budget of the outer layer. The mechanism is simple; the
discipline is not.

## The nesting model

```text
┌──────────────────────── Request boundary (owner: transport) ────────────────┐
│  catches everything; sets status; redacts; attaches requestId                 │
│  ┌──────────────────── Application boundary (owner: service) ─────────────┐  │
│  │  owns the unit of work; commits/rolls back; compensates                 │  │
│  │  ┌──────────────── Module boundary (owner: repository) ──────────────┐  │  │
│  │  │  translates driver error → domain error; preserves cause         │  │  │
│  │  │  ┌──────────────── Function boundary (owner: helper) ─────────┐  │  │  │
│  │  │  │  absorbs one specific, expected error with a safe default  │  │  │  │
│  │  │  └────────────────────────────────────────────────────────────┘  │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

An error travels **outward** until it reaches its owner. Each inner boundary may **enrich** or
**absorb** (only if it owns the fallback); it must not **terminate** a decision that belongs outward.

## The three laws of nesting

### Law 1 — An inner boundary may only absorb what it fully owns

A function boundary may absorb `ENOENT` when *this function's contract* says "missing cache = miss."
It may not absorb a DB write failure because the caller's contract says "the write happened."

```ts
// ✅ Absorb: the function's own contract defines the fallback.
function readCachedConfig(path: string): Config | null {
  try {
    return decode(readFileSync(path));
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null; // exact, owned
    throw err; // anything else is not this function's to handle
  }
}
```

### Law 2 — An inner boundary must not convert failure into success the outer cannot repair

```ts
// ❌ Inner boundary marks the operation "complete" though the write failed.
async function processOrder(order: Order) {
  try {
    await db.insert(order);
  } catch {
    order.status = "done"; // ← outer layer now operates on a lie
  }
  await events.publish(order.id, "order.completed"); // publishes success for a missing row
}
```

This is the **failure→success conversion** anti-pattern. The outer boundary would have retried or
compensated had it seen the error.

### Law 3 — Exactly one boundary decides each outcome

If two nested boundaries can both convert the same error to a response, the result depends on
execution order. Assign one owner (Ch. 15.13) and let the other only enrich.

## Interaction patterns

| Inner boundary does… | Outer boundary sees… | Verdict |
| -------------------- | -------------------- | ------- |
| Absorbs an owned, expected error | Nothing | ✅ Correct (contract-defined fallback) |
| Enriches (`throw new X(..., { cause })`) | Translated error with cause | ✅ Correct |
| Retries | Success or final error | ⚠️ Only if inner owns retry budget |
| Logs + rethrows unchanged | Same error, noisy logs | ❌ Duplicate handling |
| Swallows everything | Success | ❌ Failure→success conversion |
| Catches `Error` and replies HTTP | — | ❌ Boundary at wrong layer |

## Worked example: three boundaries, one failure

A request updates a user's email. The repository hits `SQLSTATE 23505`. Watch it travel:

```ts
// 1. Function boundary (helper) — adds context, decides nothing.
function normalizeEmail(email: string): string {
  try {
    return validator.normalize(email);
  } catch (err) {
    throw new ValueError("EMAIL_INVALID", { cause: err }); // enrich only
  }
}

// 2. Module boundary (repository) — translates driver error, preserves cause.
async function updateEmail(id: string, email: string): Promise<void> {
  try {
    await db.query("update users set email=$1 where id=$2", [email, id]);
  } catch (err) {
    if (err instanceof pg.errors.UniqueViolation) {
      throw new DomainError("EMAIL_ALREADY_USED", { cause: err }); // 23505 → domain
    }
    throw new InfrastructureError("DB_WRITE_FAILED", { transient: true, cause: err });
  }
}

// 3. Request boundary — owns the transport decision.
app.put("/users/:id/email", async (req, res) => {
  try {
    await updateEmail(req.params.id, req.body.email);
    res.status(204).end();
  } catch (err) {
    if (err instanceof ValueError) return res.status(422).json(problem(err));
    if (err.code === "EMAIL_ALREADY_USED") return res.status(409).json(problem(err));
    res.status(500).json(problem(new AppError("INTERNAL_ERROR")));
  }
});
```

The inner boundaries each added exactly what they own; only the request boundary decided the
status. The raw `23505` never left the repository.

## Ordering and scope pitfalls

- **Broad before specific.** Catching `Error` before a typed subclass makes the subclass branch
  unreachable (Ch. 12.16).
- **Boundary crossing an `await`.** In async code, a `try` around a non-awaited promise catches
  nothing; the rejection becomes detached (Ch. 31).
- **Cleanup vs decision.** `finally`/`defer` belongs to the innermost scope that acquired the
  resource, but it must not decide the outcome (Ch. 14).
- **Nested transactions/savepoints.** An inner savepoint rollback may leave the outer transaction
  valid; do not treat it as a full rollback (Ch. 23.5).

```python
# Async pitfall: the try does not cover the awaited rejection.
async def handler():
    try:
        task = asyncio.create_task(do_work())   # not awaited here
    except Exception:
        pass                                     # never triggered on task failure
    await task                                   # failure surfaces HERE, outside the try
```

## Nested retries

Nested boundaries that both retry multiply attempts (Ch. 27.17). If the integration boundary
retries 3× and the job boundary retries 3×, a failing dependency gets 9 calls.

```text
Integration boundary: 3 attempts
Job boundary:         3 attempts
Effective attempts:   3 × 3 = 9  → retry amplification
```

Rule: **retry at exactly one layer** — usually the layer that owns the deadline and the idempotency
guarantee (commonly the job or the outermost integration boundary), never both.

## Key data / numbers

- React: an error boundary does **not** catch errors in event handlers, `setTimeout`, promises, or
  server-side rendering — each needs its own containment.
- Java: catching `Exception` before `SQLException` is a compile error (unreachable) — a compiler
  assist for ordering (Ch. 7.18).
- Go: `defer` runs even on panic, but a recovered panic at an inner boundary can hide a bug — only
  recover at process/job boundaries.

## Real-world use case — Checkout

`Checkout` had a repository that caught *all* exceptions and returned `null` on failure. When the
`INSERT INTO payments` hit `23505` (duplicate idempotency key), the repository returned `null`,
the service interpreted "no payment row" as "create one," and re-attempted — producing a second
charge attempt. The nested-boundary bug: the inner `catch` converted a **conflict** into "not
found." The fix: the repository translates `23505` to `DuplicatePayment` and preserves the cause;
the service treats it as a **replay** and returns the original result.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Let each inner boundary add only what it owns | Swallow at an inner layer what an outer owns |
| Enrich with `cause`, decide once | Decide the same outcome at multiple levels |
| Keep one retry owner | Retry at every nesting level |
| Order specific catches before broad ones | Catch `Error`/`Exception` first |

## Common mistakes

- **Inner catch converts conflict → null** (as in Checkout above).
- **Catch-and-rethrow at every level**, duplicating logs and cost.
- **Recovered panic inside a library** hiding a programming bug from the process boundary.
- **Nested retry** tripling the load on a struggling dependency.

## Checklist

- [ ] Each nested boundary absorbs only errors its own contract defines.
- [ ] No inner boundary converts failure into success.
- [ ] Exactly one boundary decides each outcome.
- [ ] Retries are owned at exactly one level.
- [ ] Catch ordering is specific → broad.

## Related

- [Ownership, Granularity, and Fallback Behavior](../01-concepts/04-ownership-granularity-and-fallback.md)
- [Preserving Cause and Avoiding Circular Chains](../../16-error-translation-and-normalization/02-deep-dive/02-preserving-cause-and-circular-chains.md)
- [Part XII — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
