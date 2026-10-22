# Where Error-Handling Code Belongs

> Part XVII · Chapter 45 · Sections 45.1, 45.16 · _Estimated reading time: 14 min_
> **Prerequisite:** [Layered Error-Handling Architecture](../../../part-04-architecture/09-layered-error-handling-architecture/README.md)

## In one sentence

Error-handling code belongs in the module that **owns the decision** it implements — error
*definitions* live where the failure condition is recognized, error *handling* lives where the
fallback response is chosen — and those two modules are almost never the same file.

## Why this matters in production

When placement is ad hoc, three production symptoms appear within quarters:

- **Ownership ambiguity.** A `PAYMENT_CARD_DECLINED` code is edited by four teams because it
  sits in a shared `utils/errors.ts` nobody owns. Deprecation becomes impossible.
- **Layer inversion.** Domain services import HTTP status maps to decide what to throw, so a
  "pure" business-rule change now requires the API layer — and a domain test needs an HTTP mock.
- **Invisible policy.** Retry logic is pasted into six call sites; one copy gets a fix (jitter),
  five do not, and a provider incident becomes a retry storm.

The cost is not aesthetic. Misplaced error code converts local changes into cross-team changes
and turns policy fixes into whack-a-mole.

## Core concept: the two placement rules

**Rule 1 — Define errors where the condition is recognized.**

The module that can *detect* a condition is the module that defines its error type and code. If
only the repository layer can observe a Postgres unique violation, the mapping from
`SQLSTATE 23505` to `PROJECT_SLUG_TAKEN` belongs in the repository/infra adapter — not in the
domain, not in the controller, not in a shared utility.

**Rule 2 — Handle errors where the fallback is owned.**

The module that chooses what happens next — retry, degrade, return 409, dead-letter the job —
is the module whose fallback policy it is. A controller owns the HTTP fallback (status + body).
A worker wrapper owns the job fallback (retry vs DLQ). A saga step owns its compensation.

```text
        detects condition              chooses fallback              emits contract
 infra adapter ──────────────▶ domain/application ──────────────▶ transport handler
 (SQLSTATE 23505 →            (slug taken is a                 (409 + RFC 9457
  PROJECT_SLUG_TAKEN)          business outcome, not             envelope, code
                               an exception to swallow)          preserved)
```

## Ownership boundaries (45.16)

Every error code has exactly **one owning module**. Ownership answers three questions without a
meeting: who may change the code's meaning, who reviews its deprecation, who is paged when it
fires at 3 a.m.

| Concern | Owner | Example at Acme SaaS |
| ------- | ----- | -------------------- |
| Error primitive (`AppError`, `Result`) | Shared kernel | `@acme/errors-core` |
| Domain error code | Feature module | `checkout/errors.ts` owns `CHECKOUT_CARD_DECLINED` |
| Dependency translation | Infra adapter | `infra/postgres/errors.ts` owns `23505 → *_TAKEN` |
| HTTP envelope | Transport handler | `http/error-handler.ts` |
| Retry policy | Resilience module | `resilience/policies.ts` owns Stripe retry |
| Job failure contract | Worker boundary | `jobs/runner.ts` owns retry-vs-DLQ |

> **Rule of thumb.** If you cannot name the owning module for a code in under a minute, the code
> has no owner — and an unowned code is a code that will never be deprecated.

## How it works (mechanics)

For any new error condition, walk this sequence:

1. **Where is it detected?** That module defines the type/code (Rule 1).
2. **Does it need translation from a foreign format?** The detecting infra adapter owns the
   translation table.
3. **Who decides the outcome?** That module owns the handling (Rule 2): catch-and-translate,
   catch-and-retry, catch-and-degrade, or propagate.
4. **Who speaks to the outside?** The boundary module (HTTP handler, job runner, webhook ack)
   owns serialization — and nothing above it re-serializes.
5. **Who can change any of it?** Write the owning module down in the registry next to the code.

## Worked example

```ts
// checkout/errors.ts — OWNED by the Checkout feature module.
// Rule 1: Checkout recognizes "card declined" as a business outcome.
import { AppError } from "../../kernel/errors-core";

export class CardDeclinedError extends AppError {
  readonly code = "CHECKOUT_CARD_DECLINED" as const;
  readonly httpStatus = 402; // metadata travels with the definition
  readonly retryable = false;
  constructor(readonly declineReason: string, cause?: unknown) {
    super("Payment card was declined", { cause });
  }
}

// infra/stripe/errors.ts — OWNED by the Stripe adapter.
// Rule 1 again: only this adapter sees Stripe's error shape.
import { CardDeclinedError } from "../../checkout/errors";

export function fromStripeError(err: unknown): AppError {
  if (isStripeCardError(err)) {
    return new CardDeclinedError(err.code, err); // translation, cause preserved
  }
  return new StripeUnavailableError(err); // 5xx/timeouts → retryable class
}

// http/handlers/create-checkout.ts — OWNED by the transport layer.
// Rule 2: the HTTP boundary owns the client-facing fallback.
router.post("/checkouts", async (req, res, next) => {
  try {
    res.status(201).json(await checkoutService.create(req.body, req.ctx));
  } catch (err) {
    return next(err); // do NOT serialize here; the boundary handler owns it
  }
});
```

No layer above the adapter knows Stripe exists; no layer below the router knows RFC 9457 exists.

## Key data

- **Dependency direction that works:** transport → application → domain → kernel. Reversing any
  edge is how cycles begin (see [circular dependency avoidance](../02-deep-dive/01-circular-dependency-avoidance.md)).
- **Typical split for a 50-code SaaS:** ~10 codes in kernel-adjacent shared modules, ~30 across
  4–8 feature modules, ~10 inside infra adapters. If one file holds more than ~15 codes, it is
  almost certainly a god module (45.13).
- **Review cost:** a code with a named owning module is reviewed by 1 team; an unowned shared
  code averages reviews from 3+ teams — measured informally across multiple Acme-scale codebases
  as the difference between same-day and multi-week deprecation.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` initially threw errors from the Stripe adapter directly in the HTTP
handler, with the HTTP status decided inline. Symptom: two Stripe failure modes both returned
`500`, so Stripe's automatic webhook retry (which backs off on non-2xx) hammered Acme for hours
during a single card-declined burst. Fix: the adapter learned to *define* `WebhookSignatureInvalid`
(400, non-retryable) versus `StripeUnavailable` (503, retryable); the transport boundary learned
to *handle* them per the registry. Result: Stripe stopped retrying invalid signatures (non-2xx
with permanent semantics) and kept retrying transient 503s — webhook backlog cleared in minutes
instead of hours.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Define + handle in one shared module | Fast to start | Unowned codes, layer inversion, cycles | Toy projects only |
| Define at detection site, handle at fallback site (recommended) | Clear ownership, one-way deps, testable domain | More files, more navigation | Default for any product past MVP |
| Define centrally, handle centrally | Uniform | Central team becomes a bottleneck; domain loses meaning | Never fully; only the kernel is central |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name an owning module for every error code | Park new codes in a global `errors.ts` |
| Let the infra adapter own foreign-error translation | Import driver types into the domain |
| Let the boundary own the client-facing shape | Serialize errors in every controller |
| Keep detection and fallback rules documented together | Assume ownership is "obvious" |

## Common mistakes

- **Controller-defined domain codes.** The controller can detect a missing field, but "slug
  taken" is not a controller concept. Codes defined at the wrong layer get re-thrown and
  re-translated endlessly.
- **Adapters that handle instead of translate.** An adapter that retries *and* maps *and*
  serializes owns three decisions it cannot see the context for. Translate only; let the policy
  module retry.
- **"Temporary" global placement.** The global file is a one-way trip. Extract on day one, even
  if the extract is three lines in a feature folder.

## Checklist

- [ ] Every error code in the codebase maps to exactly one owning module.
- [ ] No domain file imports from `infra/` or `http/`.
- [ ] Each adapter owns its translation table and nothing else.
- [ ] Retry/fallback decisions are made in one policy module per dependency, not per call site.
- [ ] A new engineer can name the owner of any code from the registry alone.

## Related

- [Shared Kernel vs App-Specific Code](./02-shared-kernel-vs-app-specific.md)
- [Circular Dependency Avoidance](../02-deep-dive/01-circular-dependency-avoidance.md)
- [Acme SaaS Error Module Tree](../03-practical-examples/01-acme-error-module-tree.md)
- [Glossary: error boundary, error translation](../../../GLOSSARY.md)
