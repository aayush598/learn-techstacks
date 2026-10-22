# Feature Modules, Navigability, and the Standard Directory Structure

> Part XVII · Chapter 45 · Sections 45.17, 45.19, 45.20 · _Estimated reading time: 15 min_
> **Prerequisite:** [Supporting Modules](./04-supporting-modules-registries-mappings-retries-serialization.md)

## In one sentence

Independent feature modules own their error code end-to-end behind a narrow public surface, and
the whole system is laid out in a **standard directory structure** whose real purpose is
navigability: any engineer finds any error decision in under a minute.

## Why this matters in production

Two failure modes kill error-handling systems after they "work":

- **Feature coupling via shared error files.** `Checkout` and `ExportJob` both import from
  `shared/errors/index.ts`. A change for one PR touches the shared barrel, so the other team's
  CI runs, review queues grow, and someone eventually adds `if (code.startsWith("CHECKOUT_"))`
  inside a shared helper. The shared file has become a coordination tax *and* a hidden coupling
  hub.
- **Archaeology.** A support ticket says customers see `EXPORT_ROW_LIMIT_EXCEEDED` with the
  wrong limit. Nobody can find where the message is produced; it takes 40 minutes across four
  files. Multiply by every ticket. Navigability is not cosmetic — it is mean-time-to-understand,
  which is the dominant cost of error handling after the first year.

## Core concept: feature-owned error modules (45.17)

A feature module (`checkout/`, `export/`, `agent/`, `webhooks/`) is the unit of ownership. For
errors it follows three rules:

1. **Owns its codes.** All `CHECKOUT_*` codes are defined in `checkout/errors.ts` and exported
   through `checkout/index.ts` only as types/classes — never re-exported by a global barrel.
2. **Owns its translations that are feature-shaped.** Vendor mapping that produces *feature*
   codes lives in the feature's own adapter subfolder or in the shared vendor adapter, owned by
   agreement — but the *code* is still feature-owned.
3. **Owns its failures' meaning.** Whether `EXPORT_ROW_LIMIT_EXCEEDED` is retryable (it is not)
  is a feature decision, stamped at the definition site.

Public surface discipline: `checkout/index.ts` exports the service API and the error *types*
consumers may catch. It does not export internal helper errors (`CheckoutInternalAssert`), so
other modules cannot depend on internals you meant to keep private.

## Core concept: navigability rules (45.19)

Navigability is engineered with four cheap conventions:

| Convention | Rule | Effect |
| ---------- | ---- | ------ |
| **Prefix every code with its owner** | `CHECKOUT_*`, `EXPORT_*`, `AGENT_*`, `DEP_STRIPE_*` | `grep -r "CHECKOUT_"` = the feature's error surface; ownership is visible in the code string |
| **One `errors.ts` per feature folder** | Never a second error file in a feature | "Where are X errors?" has a fixed answer pattern |
| **File-per-error only above ~20 codes** | Grouped by default; split when the file outgrows review comfort | Avoids both 3-line file explosion and 800-line god files |
| **Names state the condition, not the handling** | `CardDeclinedError`, not `HandlePaymentFail` | The same error can be handled differently in two transports |

A one-minute test for any repo: pick a code at random from a production log line. Can a new
engineer find its definition, its registry entry, and its HTTP mapping in 60 seconds using only
naming conventions? If not, fix naming before adding more codes.

## The standard directory structure (45.20)

```text
src/
├── kernel/                        # ZONE 1 — shared primitives (or packages/errors-core)
│   ├── app-error.ts               #   AppError base, category enum
│   ├── result.ts                  #   Result<T,E> if used
│   └── redact.ts                  #   context sanitization
├── shared/
│   ├── registry/error-codes.ts    # 45.7 — pure data: code → metadata
│   └── resilience/retry-policies.ts  # 45.9 — named retry policies
├── features/                      # ZONE 2 — one folder per business capability
│   ├── checkout/
│   │   ├── errors.ts              #   CHECKOUT_* codes (owned here)
│   │   ├── checkout.service.ts
│   │   └── index.ts               #   public surface: service + error types
│   ├── export/
│   │   ├── errors.ts              #   EXPORT_* codes
│   │   └── export.job.ts          #   ExportJob workflow
│   └── agent/
│       └── errors.ts              #   AGENT_* / LLM_* codes
├── infra/                         # ZONE 3 — one folder per dependency
│   ├── postgres/errors.ts         #   SQLSTATE → app errors (mapping module)
│   ├── stripe/errors.ts           #   Stripe → app errors
│   ├── s3/errors.ts
│   └── llm/errors.ts              #   provider → app errors (AgentRun)
├── transports/                    # ZONE 4 — one folder per external-facing runtime
│   ├── http/
│   │   ├── error-handler.ts       #   global handler (catch-all boundary)
│   │   └── serialize-problem.ts   # 45.11 — RFC 9457 serializer (only one)
│   ├── jobs/
│   │   ├── runner.ts              #   per-job boundary: retry vs DLQ
│   │   └── serialize-failure.ts   #   DLQ payload serializer
│   └── webhooks/
│       └── ack.ts                 #   provider ack/nack mapping
└── workflows/                     # 45.10 — multi-step sagas + compensations
    └── checkout-saga/
        ├── steps.ts
        └── compensations.ts       #   refund, release-hold — colocated with steps
```

Sizing guidance: an MVP can collapse `shared/` into `kernel/` and put all features in one
`features/` folder with three `errors.ts` files. The structure's value is the **slots**, not the
file count — grow into the slots, never invent new top-level folders for error code.

## Worked example — the one-minute lookup

Support ticket: `code=EXPORT_ROW_LIMIT_EXCEEDED, limit=100000 but customer is on the Pro plan`.

```text
1. grep "EXPORT_ROW_LIMIT_EXCEEDED"  → features/export/errors.ts (definition + owner)
2. open features/export/errors.ts    → sees limit taken from plan entitlement, not hard-coded
3. grep registry                     → shared/registry/error-codes.ts → 422, not retryable
4. grep serializer path              → transports/http/serialize-problem.ts (one file)
Total: 4 files, ~3 minutes first time, ~1 minute once you know the map.
```

Compare with the unmapped variant: a single `shared/errors/index.ts` (900 lines), an inline
`res.status(422)` in two controllers with different messages, and a job serializer that drops
the `limit` field entirely. Same bug, ~40 minutes to root cause.

## Key data

- **Prefix scheme at Acme:** `CHECKOUT_`, `PROJECT_`, `EXPORT_`, `AGENT_`, `WEBHOOK_`, `AUTH_`,
  `DEP_<VENDOR>_` (adapter-owned), `INTERNAL_` (kernel/infra unexpected). Seven prefixes covered
  100% of codes emitted in production logs over a quarter.
- **Feature folder sizing:** 1 `errors.ts` per feature; split to file-per-error above ~20 codes
  or ~300 lines. ExportJob's module: 14 codes, 1 file, 96 lines.
- **Barrel rule:** global `index.ts` re-exports *features' public APIs* but **never** re-exports
  error modules — cross-feature error imports go through the owning feature's `index.ts`.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` and `Checkout` both needed "provider unavailable" handling. With the
standard structure, each defined its own code (`WEBHOOK_DELIVERY_DEFERRED`,
`DEP_STRIPE_UNAVAILABLE`) sharing one adapter mapping and one retry policy — duplication of the
*policy* was impossible because the policy lives in `shared/resilience/retry-policies.ts`, while
*meaning* stayed separate: deferring a webhook delivery is not the same outcome as failing a
checkout. Six months later the team added Adyen as a second payment provider: a new
`infra/aden/` folder plus two feature codes — zero changes to the registry schema, serializers,
or retry module. The structure paid for itself in the vendor-addition PR, which reviewers
described as "boring," the highest praise infrastructure can receive.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Feature-owned modules + standard tree (recommended) | Ownership visible; fast lookup; parallel teams | More folders; onboarding to the map | Any multi-team or multi-feature product |
| Flat `shared/errors` catalog | Simple initially | Coordination tax; hidden coupling | Single-author prototypes |
| Layer-only tree (`errors/`, `handlers/`, `mappers/` by layer) | Familiar to layered teams | Cannot see feature ownership; grep mixes domains | Avoid once features outnumber ~3 |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Prefix every code with its owning feature | Use generic prefixes (`ERR_`, `E1002`) |
| Keep one `errors.ts` per feature folder | Scatter error classes across service files |
| Export error types only through the owning feature's `index.ts` | Re-export all errors from a global barrel |
| Grow into the standard slots | Create new top-level folders per new error idea |

## Common mistakes

- **Premature file-per-error.** Twenty 4-line files are harder to navigate than one 90-line
  grouped file. Split on review pain, not on principle.
- **Global barrel creep.** `shared/index.ts` re-exports everything "for convenience" — within a
  quarter, features import each other's internals. Ban error re-exports in the barrel.
- **Prefix without ownership.** A prefix that three modules may use is decoration. Enforce
  prefix↔folder mapping in review (or a lint rule matching prefix to import path).

## Checklist

- [ ] Every code's prefix matches its owning feature/adapter folder.
- [ ] The standard tree's slots exist in your repo, even if some hold only one file.
- [ ] One-minute lookup test passed for three random codes by someone outside the owning team.
- [ ] No global barrel re-exports error modules.
- [ ] Compensation functions sit next to their saga steps.

## Related

- [Where Error-Handling Code Belongs](./01-where-error-code-belongs.md)
- [Avoiding a Global God Module](../02-deep-dive/02-avoiding-god-module-and-duplication.md)
- [Acme SaaS Error Module Tree](../03-practical-examples/01-acme-error-module-tree.md)
- [Directory Structure Reference](../05-reference/README.md)
