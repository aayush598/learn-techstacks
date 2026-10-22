# Handle Once, Flow Consistently

> Part IV · Chapter 9 · Sections 9.19–9.20 · _Estimated reading time: 16 min_
> **Prerequisite:** [Where to Handle, Translate, and Propagate](./03-where-to-handle-translate-and-propagate.md)

## In one sentence

Every error has **exactly one layer that decides its outcome**, and the same category of failure
must produce the **same external shape no matter which entry point** it arrived through.

## Why this matters in production

Duplicate handling is the tax you pay for layered code with no ownership rules:

- **Double retry** — controller retries and application retries: 3 × 3 = 9 upstream calls, and a
  non-idempotent `POST /checkouts` creates up to 9 charges.
- **Double translation** — repository maps `23505` → `Conflict`, then a middleware re-maps the
  already-translated error "just in case," dropping the original code and turning a `409` into a
  `500`.
- **Double response shaping** — a filter writes a `409` body, then the default handler writes a
  second body: corrupted JSON or `ERR_HTTP_HEADERS_SENT`.

And when entry points disagree — HTTP returns `409`, the queue consumer retries the same
condition forever, the scheduled task silently skips it — operators cannot trust alerts and
clients cannot trust the API. **Consistency is not aesthetics; it is the contract.**

## Core concept — the handle-once ledger

Maintain one table (in your architecture doc, Chapter 55) that answers three questions per error:

| Error code | Origin layer | **Handling layer (exactly one)** | External shape (HTTP) | External shape (job) |
| ---------- | ------------ | ------------------------------- | --------------------- | -------------------- |
| `WORKSPACE_SLUG_TAKEN` | repository | application (abort) | `409` + code | terminal `failed`, no retry |
| `UPSTREAM_RATE_LIMITED` | integration | application (one retry, honor `Retry-After`) | `429` | delayed retry, backoff |
| `DB_UNAVAILABLE` | infrastructure | application (retry if idempotent, else `503`) | `503` + `Retry-After` | retry with backoff |
| `TRIAL_NOT_ELIGIBLE` | domain | transport (render, nothing to do) | `422` | terminal, business event |
| unclassified | anywhere | process/global handler | `500` + correlation ID | retry once, then DLQ |

Three invariants:

1. **One decision-maker.** For a given code, exactly one layer contains the `switch`/`if` that
   chooses retry, compensation, degradation, or termination.
2. **Translators never decide.** Translation layers map representations; they never contain
   `if (retry)`.
3. **Entry points converge.** HTTP, queue, and scheduler paths all funnel into the same
   application service, so they inherit the same decision; only the *rendering* differs.

## How it works — detecting duplicate handling

Search your codebase for the same decision expressed twice:

```text
grep -rn "Retry-After\|retryable\|maxAttempts\|backoff" src/ --include="*.ts"
```

If two layers define retry counts for the same operation, one is stale. Also watch for these
duplicate shapes:

```ts
// ❌ DUPLICATE: retry in controller AND in the application service
app.post("/checkouts", async (req, res, next) => {
  try { res.json(await retry(() => createCheckout(req.body), { attempts: 3 })); }
  catch (e) { next(e); }
});
// application service also does: for (let i = 0; i < 3; i++) { try { ... } catch { } }

// ✅ SINGLE OWNER: controller maps only; the service owns the decision
app.post("/checkouts", async (req, res, next) => {
  try { res.status(201).json(await createCheckout(req.body)); }
  catch (e) { next(toProblem(e)); }   // toProblem never retries
});
```

## Consistent end-to-end flow

Define one canonical flow and reuse it for every entry point:

```text
 entry ──▶ detect ──▶ classify ──▶ translate at boundary ──▶ decide (ONE layer)
                                                            │
                     ┌────────────── external render ◀──────┤
                     │  HTTP: RFC 9457 envelope + status    │
                     │  job : attempt++, backoff / DLQ      │
                     └──────────── terminal record: same code, same correlation ID
```

The invariant to test: **pick any error code, hit it via HTTP and via a queued job, and the code
in the final record must be identical** — only the envelope differs.

## Worked example — one error, two entry points

```ts
// Shared decision (application layer) — used by BOTH the HTTP route and the worker
export async function runExport(cmd: ExportCommand): Promise<ExportOutcome> {
  try {
    await exporter.run(cmd);            // domain + infra errors propagate here
  } catch (err) {
    const e = normalize(err);           // one translator
    if (isRetryable(e)) throw e;        // ONE decision: let the retry owner act
    await exportsRepo.markFailed(cmd.id, e.code, e.detail);
    return { status: "failed", code: e.code };
  }
  return { status: "ok" };
}
```

```ts
// HTTP renderer
catch (e) { res.status(statusFor(e.code)).json(problem(e, req.id)); }

// Worker renderer (same error, job-shaped outcome)
catch (e) {
  if (isRetryable(e)) return attempt.retry({ delayMs: backoff(attempt.n) });
  return attempt.fail({ code: e.code, dlq: attempt.n >= MAX_ATTEMPTS });
}
```

Same classifier, same code, two renderers — **one decision, consistent shapes**.

## Key data / numbers

- Retry amplification: 3 attempts in two layers = up to **9** upstream calls; with three layers,
  27. Retry ownership must be a single line item in your ledger.
- HTTP shapes for the same underlying codes: conflict `409`, semantic `422`, rate limit `429` +
  `Retry-After`, upstream outage `503` + `Retry-After`, unclassified `500`.
- Job shapes for the same codes: retryable → delayed retry (recommendation: exponential backoff
  base ~2 s, factor 2, jitter, **max 5 attempts**); terminal → `failed`/DLQ immediately.
- Headers that must not be written twice: `Content-Type` — a second response attempt raises
  Node's `ERR_HTTP_HEADERS_SENT`.

## Real-world use case — Acme SaaS `ExportJob` + `POST /exports`

Both entry points created an export. The HTTP path checked `isRetryable` in the route; the queue
path checked a *different* (older) predicate in the worker. Result: a `DB_UNAVAILABLE` during a
run was retried by HTTP clients **and** re-queued by the worker, producing duplicate export rows
and two `failed` records with different codes for one incident.

Fix: move classification and the retry decision into `runExport` (shown above), leaving HTTP to
render status and the worker to schedule attempts. Cross-entry-point duplicate rows stopped
immediately, and dashboards could finally group by a single stable code.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single decision layer + per-entry renderers | No duplication, consistent contracts | Requires the shared application service | Default |
| Each entry point decides independently | Ship fast | Drift, double retries, inconsistent codes | Not beyond an MVP |
| Global handler decides everything | One place | Cannot see business state (see Ch. 10) | Never for business codes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep one handling layer per code in a ledger | Let controller and service both retry |
| Route every entry point through the same service | Re-implement decisions in workers |
| Render per protocol (HTTP vs job) after deciding | Let rendering layers re-classify |
| Assert identical codes across entry points in tests | Assume entry points drift "won't happen" |

## Common mistakes

- **Fixing drift with more code at the edge** — the fix is centralizing the decision, not adding
  a third translator.
- **Two ledgers** (API docs vs worker docs) that disagree — one source of truth (Chapter 55).
- **Retrying in a `finally`-style wrapper "for safety"** — safety wrappers are duplicate
  handlers; delete them.

## Checklist

- [ ] Every error code has exactly one handling layer recorded.
- [ ] A test asserts the same code for one fault triggered via HTTP and via the queue.
- [ ] Retry counts exist in exactly one module per operation.
- [ ] No middleware/filter re-translates an already-translated application error.

## Related

- [Where to Handle, Translate, and Propagate](./03-where-to-handle-translate-and-propagate.md)
- [Preventing Leakage Across Layers](./04-preventing-leakage-across-layers.md)
- [Preventing Double Handling and Failures During Handling](../../11-the-error-lifecycle/02-deep-dive/01-double-handling-and-error-during-handling.md)
- [Chapter 11 — The Error Lifecycle](../../11-the-error-lifecycle/README.md)
