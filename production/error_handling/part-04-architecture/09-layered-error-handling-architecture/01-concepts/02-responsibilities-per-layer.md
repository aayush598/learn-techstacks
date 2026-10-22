# Responsibilities per Layer

> Part IV · Chapter 9 · Section 9.13 · _Estimated reading time: 16 min_
> **Prerequisite:** [The Layers of an Error-Handling Architecture](./01-layered-architecture-overview.md)

## In one sentence

Each layer gets **exactly one error-handling job** — detect, translate, decide, or render — and
the boundary between two layers is where the job changes hands.

## Why this matters in production

A layer with no defined error job becomes a dumping ground. Concretely:

- If the **controller** has no rule, developers put retries there, and retries multiply with every
  caller.
- If the **repository** has no translation rule, driver semantics leak upward and every caller
  re-parses `SQLSTATE`.
- If the **global handler** has no rule, it starts making business decisions it cannot know.

Assigning one job per layer is the cheapest way to make error handling **predictable** and
**reviewable**.

## The one-job-per-layer table

| Layer | Error job (verb) | What it may do | It must NOT |
| ----- | ---------------- | -------------- | ----------- |
| **Transport** | **Reject early** | Return `400/401/403/413/415/429`; abort before app code | Interpret business meaning |
| **Controller** | **Map** | Convert outcome → status/body; attach request ID | Retry; catch to log-and-rethrow |
| **Application service** | **Decide** | Choose retry/compensate/abort; own transaction outcome | Leak vendor/HTTP types to domain |
| **Domain** | **Declare** | Raise invariant-rule errors as domain types | Know about persistence or transport |
| **Repository** | **Translate** | Driver error → persistence error; distinguish no-row vs failure | Decide business policy |
| **Infrastructure** | **Surface** | Produce operational errors with cause preserved | Imply domain meaning |
| **Integration** | **Normalize** | Vendor error → stable internal code | Expose vendor shape to callers |
| **Background worker** | **Classify + schedule** | Retryable vs terminal, backoff, DLQ | Contain domain rules |
| **Scheduled task** | **Guard** | Prevent overlap; idempotent re-run | Assume the previous run succeeded |
| **Bootstrap** | **Halt** | Fail fast on init error | Start serving half-wired |
| **Process boundary** | **Terminate** | Log safely, flush, exit non-zero | Attempt in-process recovery |

> The rule of thumb: **a layer either changes an error's *representation* (translate) or changes
> its *outcome* (handle).** It should not do both silently.

## Detect vs translate vs decide vs render

```text
DETECT     ── notice the condition (throw or return an error)      → repo, domain, integration
TRANSLATE  ── change representation without changing meaning       → repo, integration, controller
DECIDE     ── choose the outcome (retry/compensate/fail)           → application service, worker
RENDER     ── present the outcome to the outside world             → transport, controller, UI
```

Each layer occupies one of these roles for a given failure. The same failure is *detected* low,
*translated* at boundaries, *decided* once, and *rendered* once.

## Worked example — mapping one failure across layers

A request creates a workspace with a duplicate slug.

```text
Update  → DETECT      Postgres raises SQLSTATE 23505              (infrastructure)
        → TRANSLATE   repo: DuplicateKey("workspaces_slug_key")   (repository)
        → DECIDE      app: this is a business conflict → abort    (application service)
        → DECLARE     domain: SlugAlreadyTaken (domain outcome)
        → MAP         controller: SlugAlreadyTaken → 409          (controller)
        → RENDER      transport: body { code: "SLUG_TAKEN" }      (transport)
```

Six layers, six distinct jobs, **one decision**. No layer both decides and renders.

## How to use this table in code review

Ask three questions of any changed handler:

1. **Which layer is this?** If the answer is ambiguous, the code is in the wrong place.
2. **What is its job here — detect, translate, decide, or render?**
3. **Is any *other* layer doing the same job for this error?** If yes, delete one.

## Real-world use case — Checkout (Stripe decline)

An Acme `Checkout` charge fails with a declined card.

| Layer | Correct job | Anti-pattern |
| ----- | ----------- | ------------ |
| Integration | Normalize `card_declined` → `PAYMENT_CARD_DECLINED` | Re-throw raw Stripe object |
| Application | Decide: **no retry**, mark payment `failed` | Retry a decline 3× |
| Controller | Map → `402` with code and recovery hint | Return `500` |
| Transport | Render envelope + request ID | Leak Stripe `decline_code` verbatim |

The same endpoint that elsewhere retries a `429` must **not** retry a decline — because the
*decide* job lives in one place (application) and consults classification (Part II).

## Key data / numbers

- Postgres `23505` must become a domain-level `Duplicate`/`Conflict`, never a raw `SQLSTATE`.
- HTTP mapping decisions belong only in the controller: `402` (payment required), `409`
  (conflict), `422` (semantic), `429` (rate limit).
- A repository should distinguish **`RecordNotFound`** from **`QueryFailed`** — two codes, two
  policies (404 vs 500).

## Trade-offs

| Granularity | Pros | Cons |
| ----------- | ---- | ---- |
| Strict one-job-per-layer | Predictable, reviewable | More mapping code |
| Allow controller to translate infra in MVP | Fast to ship | Leaks when you grow |

Default: strict roles for cross-cutting failures (auth, persistence, vendor); pragmatic collapse
only where a layer is trivially thin.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign one error verb per layer | Let the controller decide retries |
| Translate representation at boundaries | Translate the same thing twice |
| Keep decisions (retry/compensate) in the app service | Decide in the global handler |
| Preserve the cause while translating | Replace an error with a bare `Error("failed")` |

## Common mistakes

- **Two layers translating the same error**, so the second translation loses the first's metadata.
- **A repository deciding policy** ("if duplicate, retry once") — that is an application decision.
- **A worker re-implementing domain rules** because the application service was bypassed.

## Checklist

- [ ] Does each layer have a documented error job?
- [ ] For your top ten errors, is the *decide* job in exactly one layer?
- [ ] Does any layer both decide and render the same failure?
- [ ] Are translation points listed explicitly in your architecture doc (Ch. 55)?

## Related

- [Where to Handle, Translate, and Propagate](./03-where-to-handle-translate-and-propagate.md)
- [Layer Contracts and Translation Points](../02-deep-dive/01-layer-contracts-and-translation-points.md)
- [Part VI — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
