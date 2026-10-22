# The Lifecycle: Origin, Detection, Representation, Classification

> Part IV · Chapter 11 · Sections 11.1–11.4 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 9 — Layered Architecture](../../09-layered-error-handling-architecture/README.md)

## In one sentence

Every error begins at an **origin**, becomes real at a **detection point**, takes a **machine
representation**, and receives a **classification** — the first four stages that determine
everything the rest of the system can do with it.

## Why this matters in production

Failures at these first stages are silent and expensive. An error that is never *detected* sits
as a wrong value until it corrupts data. An error represented as `Error("failed")` is
unclassifiable, so every downstream stage guesses. An error classified by message text drifts
with every wording change. The lifecycle makes each of these a **deliberate, named step** with an
owner — so downstream stages can be mechanical.

## The lifecycle diagram

```text
                 ┌──────────────── THE ERROR LIFECYCLE ────────────────┐
                 │                                                      │
 1 ORIGIN        │  2 DETECT          3 REPRESENT         4 CLASSIFY   │
 where the       │  assertion,        AppError with       code +       │
 deviation       │  validation,       stable code,        metadata:    │
 starts          │  thrown check,     cause slot          category,    │
 (bug, input,    │  driver error      (Part III)          retryable,   │
 dependency)     │                                            severity  │
                 │         │                │                   │      │
                 │         ▼                ▼                   ▼      │
 5 ENRICH        │  add SAFE context: operation, tenant, correlationId │
                 │                                                      │
 6 PRESERVE CAUSE│  original error attached as `cause`, never overwritten│
                 │                                                      │
 7 PROPAGATE     │  move up layers untouched (Ch. 9 verbs)              │
                 │                                                      │
 8 TRANSLATE     │  at each boundary: driver→persistence→domain→HTTP    │
                 │                                                      │
 9 DECIDE        │  ONE owner: retry / compensate / degrade / abort     │
                 │                                                      │
 10 APPLY        │  execute retries (budgeted) or compensation steps    │
                 │                                                      │
 11 RENDER       │  HTTP envelope / job attempt record / event          │
                 │                                                      │
 12 FINALIZE     │  record terminal outcome: failed / compensated / ok  │
                 │                                                      │
 13 CLEANUP      │  release tx, locks, temp files, streams (always)     │
                 │                                                      │
 14 TERMINAL     │  nothing further may change the outcome              │
                 └──────────────────────────────────────────────────────┘
```

Stages 1–4 are this file; 5–6 next; 7–10; 11–13; and 14 plus the guard rails in the fifth file.

## Stage 1 — Where errors originate (11.1)

Origins are enumerable; list them for your system:

| Origin class | Example | Owner of the origin |
| ------------ | ------- | ------------------- |
| Input from outside | malformed JSON, bad email, hostile payload | transport/controller |
| Domain computation | invariant violated, invalid transition | domain |
| Persistence | `SQLSTATE 23505`, connection reset | repository/infrastructure |
| External dependency | Stripe `402`, LLM `429`, DNS failure | integration |
| Concurrency | `40001` serialization, optimistic conflict | application/repository |
| Runtime/resource | OOM, fd exhaustion, pool saturation | infrastructure/process |
| Our own bugs | null deref, logic error | nobody — that is the point |

Knowing the origin tells you which *detection* is even possible — and which stage 9 decision
makes sense.

## Stage 2 — Detecting (11.2)

Detection is the moment the deviation becomes an error *value*: a thrown exception, a returned
`Result.Err`, a failed assertion, a driver callback error. Detection policies:

- **Detect as early as the fact is known.** A `NaN` from parsing is detected at parse, not at the
  payment gateway (Chapter 2's fail-fast).
- **Invariants are detected where they are stated** — in the domain, via explicit checks.
- **Silence is a bug.** A wrong value that is never detected is the worst lifecycle outcome: it
  becomes *data*.

```ts
// detection points are explicit and early
const amount = Money.parse(input.amount);        // throws VALIDATION_AMOUNT_INVALID (detect here)
if (amount.isZero() && !cmd.allowZero)           // domain invariant
  throw new DomainError("CHECKOUT_AMOUNT_ZERO");
```

## Stage 3 — Creating the representation (11.3)

By the time anything above the detecting layer sees it, the error must be the **standard internal
representation** (Part III): stable `code`, category, severity, `retryable`, `cause` slot,
correlation fields. The rule: **the detecting layer converts immediately** — a raw driver error
is converted in the repository, a vendor payload in the integration adapter (Chapter 9's
translation points). What travels after stage 3 is your model, not someone else's.

## Stage 4 — Classifying (11.4)

Classification attaches the axes from Part II that drive every later decision:

| Field | Drives | Example |
| ----- | ------ | ------- |
| `category` | status mapping, alert routing | `conflict`, `rate_limit`, `validation` |
| `retryable` | stage 9–10 decisions | `true` for `40001`, `false` for `402` decline |
| `severity` | paging vs ticketing | `critical` vs `expected` |
| `terminal` for jobs | DLQ vs delayed retry | `DATA_INTEGRITY` terminal |
| `public` | what the envelope may show | `false` for infra codes |

Classification happens **once**, at or immediately after representation — not re-derived per
handler (a lifecycle version of handle-once).

## Key data / numbers

- Postgres codes and their natural classifications: `23505` → conflict, permanent, not
  retryable; `40001`/`40P01` → transient, retryable; `53300` → transient, infrastructure.
- HTTP classes as classification shorthand: `4xx` = client/permanent, `429`/`503`/`504` =
  transient-ish, `500`/`502` = server, retry only when idempotent.
- gRPC: `UNAVAILABLE` (14) and `DEADLINE_EXCEEDED` (4) are the retryable-ish canon;
  `INVALID_ARGUMENT` (3), `NOT_FOUND` (5), `ALREADY_EXISTS` (6) are permanent.
- A registry-driven classification beats `instanceof` chains: same code, same verdict, everywhere
  (Chapter 8).

## Real-world use case — Acme SaaS `WebhookIngest`

A `checkout.session.completed` webhook carried an amount the tenant's plan had just downgraded
below the minimum. The domain invariant (`CHECKOUT_AMOUNT_BELOW_MINIMUM`) was *not detected* —
the code only checked amounts at creation, not on webhook replay. The error originated (stage 1)
but went undetected (stage 2), represented itself as **wrong subscription state** three weeks
later during reconciliation.

The fix was lifecycle-shaped: add an explicit detection at the webhook application service
(replay-safe invariant check), represent it as a classified `WEBHOOK_STATE_CONFLICT`
(permanent, non-retryable, `public: false`), and let stages 9–14 route it to the DLQ with an
audit record. Detection debt is the most expensive stage to repay.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Explicit stages 1–4 with a registry (recommended) | Every later stage is mechanical | Requires representation discipline | Default |
| Ad-hoc throw-and-catch | Fast per incident | Unclassifiable errors; guessing downstream | Never |
| Detect everything everywhere | Maximum safety | Duplicate detection, noisy errors | Only for invariants with data-loss risk |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Detect at the earliest sound moment | Let `NaN`/null travel to a gateway |
| Represent immediately in your model | Let raw driver/vendor objects cross stage 3 |
| Classify once, store on the error | Re-classify per handler from message text |
| Record origins in your failure inventory | Assume origins are "obvious" |

## Common mistakes

- **Representing too late** — the domain receives `unknown` because the repository passed the
  driver error through "for context."
- **Classification in the renderer** — the controller deriving retryable-ness from status codes
  instead of reading the registry.
- **Undetected business origins** — invariants checked at entry but not on asynchronous replays
  (webhooks, jobs) — the Acme case above.

## Checklist

- [ ] Your origin inventory lists input, domain, persistence, dependency, concurrency, runtime.
- [ ] Every detection point converts to the standard representation immediately.
- [ ] Classification fields (`category`, `retryable`, `severity`) come from the registry.
- [ ] Async replay paths (webhooks, jobs) re-run the same invariant detections.

## Related

- [Enrichment and Cause Preservation](./02-enriching-and-preserving-cause.md)
- [Propagation, Translation, and Recovery](./03-propagation-translation-and-recovery.md)
- [Part II — Error Taxonomy and Classification](../../../part-02-error-taxonomy/README.md)
- [Part III — Designing the Application's Error Model](../../../part-03-error-models/README.md)
