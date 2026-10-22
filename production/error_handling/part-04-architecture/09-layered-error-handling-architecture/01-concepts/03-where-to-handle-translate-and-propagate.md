# Where to Handle, Translate, and Propagate

> Part IV · Chapter 9 · Sections 9.16–9.18 · _Estimated reading time: 16 min_
> **Prerequisite:** [Responsibilities per Layer](./02-responsibilities-per-layer.md)

## In one sentence

**Handle** at the layer that owns the outcome, **translate** at every boundary the error crosses,
and **propagate** untouched everywhere else — three verbs, one job each, no overlap.

## Why this matters in production

Most error-handling chaos is not missing `try/catch`; it is the *wrong verb at the wrong layer*.
A controller "handles" a database outage by inventing a status code. A repository "handles" a
duplicate key by retrying — twice, because the application service also retries. A domain service
"translates" into HTTP codes and now nothing can reuse it from a worker.

The symptoms are predictable: **double side effects** (double charges), **meaningless 500s** for
solvable conditions, and a codebase where nobody can answer "who decides what happens to this
error?" The fix is a single decision table applied at every layer crossing.

## Core concept — the three verbs

| Verb | What changes | Who may do it | Signature in code |
| ---- | ------------ | ------------- | ----------------- |
| **Handle** | the *outcome* (retry / compensate / fail / degrade) | the layer that owns the decision: application service, worker, transport for request-shape errors | `catch` with a fallback, a status decision, or a terminal mark |
| **Translate** | the *representation*, never the meaning | the layer on the far side of a boundary: repository, integration, controller | `catch (e) { throw new DuplicateKey(...) }` with `cause` preserved |
| **Propagate** | nothing | every layer in between | no `catch`, or `catch` that only adds context and rethrows the same error |

```text
   transport ──▶ controller ──▶ application ──▶ domain ──▶ repository ──▶ infrastructure
       │             │              │             │            │               │
     RENDER        MAP           HANDLE        DECLARE     TRANSLATE        DETECT
   (4xx/5xx)   (status/body)  (retry/abort)  (rule error) (SQLSTATE→app)  (driver error)
                                   ▲                          │
                                   └──── PROPAGATE ◀───────────┘  (app errors moving up)
```

Errors travel **up** (right-to-left in the diagram); control travels **down**. At each arrow,
exactly one of the three verbs applies.

## How it works — the decision rules

**Rule 1 — Handle where the fallback is decided.** Ask: "what do we do now — retry, compensate,
degrade, or fail?" That question belongs to the layer with enough information to answer it. The
application service knows the transaction state; the worker knows the attempt count; the transport
knows nothing about business state and must not decide.

**Rule 2 — Translate where the representation changes.** A `SQLSTATE` string, a Stripe error
object, and an HTTP status are three representations of failure. Each crosses a boundary exactly
once, at the layer that owns the foreign vocabulary:

- driver → repository (`SQLSTATE 23505` → `DuplicateKey`)
- vendor → integration (`card_declined` → `PAYMENT_CARD_DECLINED`)
- outcome → controller (`SlugAlreadyTaken` → `409`)

**Rule 3 — Propagate by default.** If you cannot name a *different* outcome at this layer, do not
catch. Add context (`withOperation("createWorkspace")`) and let it travel. A catch that only logs
and rethrows is not handling; it is noise, and it is covered in Chapter 13.

**Rule 4 — One handle, many translates, zero surprises.** An error may be translated at every
boundary it crosses, but it is *handled* — its outcome decided — exactly once.

## Worked example — three failures, three correct paths

```ts
// TypeScript — Checkout POST /checkouts
// Path A: request-shape failure is HANDLED at transport/controller (never reaches app code)
//   body fails schema parse  -> 422 { code: "VALIDATION_FAILED", fields: [...] }

// Path B: domain failure is PROPAGATED up, then MAPPED by the controller
async function createCheckout(cmd: CreateCheckout) {
  const plan = await plans.get(cmd.planId);      // throws NotFound (propagated)
  if (!plan.allowsTrial(cmd.tenantId))           // domain declares
    throw new DomainError("TRIAL_NOT_ELIGIBLE"); //   propagated through app layer
  return payments.charge(cmd);                   // integration error also propagated
}

// Path C: infrastructure failure is TRANSLATED at the repository, then DECIDED by the app
try {
  await db.query("INSERT INTO checkouts ...");
} catch (e) {
  if (isUniqueViolation(e)) {                    // SQLSTATE 23505
    throw new Conflict("CHECKOUT_ALREADY_EXISTS", { cause: e });
  }
  throw new PersistenceError("CHECKOUT_WRITE_FAILED", { cause: e }); // 500-class
}
```

Then the application service — and only the application service — decides: a `Conflict` aborts, a
`PersistenceError` triggers **one** retry of the transaction if the operation is idempotent.

## Key data / numbers

- Transport-owned statuses: `400`, `401`, `403`, `405`, `413`, `415`, `429` — rejected before
  application code runs.
- Controller-owned mapping: `404` (missing aggregate), `409` (conflict/duplicate), `422`
  (semantic rule), `500` (unmapped internal), `502`/`503`/`504` (upstream, via integration).
- Repository-owned translations: `SQLSTATE 23505` → conflict, `23503` → FK violation,
  `40001`/`40P01` → retryable transaction conflict.
- Retry decisions are owned by exactly one layer; nested retries multiply latency by the product
  of attempt counts (3 × 3 = 9 upstream calls — a classic retry-amplification failure).

## Real-world use case — Acme SaaS `Checkout`

Acme's `POST /checkouts` returned `500` for every Stripe timeout **and** for duplicate
subscriptions, because the controller caught everything from the SDK. The re-layering:

1. Integration translated Stripe errors (`api_key_invalid` → `PAYMENT_CONFIG_ERROR`,
   `rate_limit` → `UPSTREAM_RATE_LIMITED`, `card_declined` → `PAYMENT_CARD_DECLINED`).
2. The application service *handled* once: `UPSTREAM_RATE_LIMITED` → one retry honoring
   `Retry-After`; `PAYMENT_CARD_DECLINED` → no retry, payment marked `failed`.
3. The controller only *mapped*: `402` with code for declines, `429` for rate limits, `503` for
   sustained provider outage.

Duplicate-subscription and timeout tickets fell to zero; timeouts became rare `429`s/`503`s that
clients could actually retry.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Verdict-by-layer (this file) | Predictable ownership, one decision point | Requires an explicit decision table | Default for any multi-layer service |
| Handle wherever convenient | Fast locally | Duplicates decisions, double side effects | Throwaway scripts only |
| Handle only at the edge | One decision point guaranteed | Too little context; cannot compensate | Not recommended except tiny services |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Handle where the outcome is decided | Handle in the controller *and* the service |
| Translate once per boundary crossed | Translate the same error twice in a row |
| Propagate when you cannot name a new outcome | `catch` just to log and rethrow |
| Keep `cause` through every translation | Replace errors with `new Error("failed")` |

## Common mistakes

- **Handling at the edge to "keep controllers thin"** — the controller now makes business
  decisions (retry vs abort) it cannot see the state for.
- **Translating inside the domain** — domain errors gain HTTP codes and become unusable from
  workers and message consumers.
- **Double handling by retry in two layers** — latency multiplies and side effects duplicate;
  detect it with a single "retry owner" line in your decision table.

## Checklist

- [ ] For your top ten errors, the table names one handling layer.
- [ ] Every foreign vocabulary (SQLSTATE, vendor codes) is translated exactly once, at its
      boundary layer.
- [ ] No `catch` block exists whose only effect is logging + rethrowing.
- [ ] Retries have exactly one owner per operation.

## Related

- [Responsibilities per Layer](./02-responsibilities-per-layer.md)
- [Preventing Leakage Across Layers](./04-preventing-leakage-across-layers.md)
- [Layer Contracts and Translation Points](../02-deep-dive/01-layer-contracts-and-translation-points.md)
- [Part VI — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
