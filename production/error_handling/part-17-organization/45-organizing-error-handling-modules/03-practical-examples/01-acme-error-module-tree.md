# Acme SaaS — The Error-Handling Module Tree

> Part XVII · Chapter 45 · Section 45.20 (applied) · _Estimated reading time: 18 min_
> **Prerequisite:** [Feature Modules, Navigability, and the Standard Directory Structure](../01-concepts/05-feature-modules-and-navigability.md)

## In one sentence

This file lays out the complete error-handling directory tree for Acme SaaS — the recurring
cast's home repo — with the actual contents of each module, so you can copy the structure and
shrink it to your project's size.

## Why this matters in production

Diagrams do not compile. Seeing the *files* — what each one contains, what it imports, what it
must never contain — is the difference between adopting a standard and re-deriving it through
six months of incidents. This tree is the reference implementation the rest of Part XVII cites.

## The tree

```text
acme/
├── packages/
│   └── errors-core/                      # ZONE 1 — versioned kernel package
│       ├── src/
│       │   ├── app-error.ts              #   AppError base + ErrorCategory
│       │   ├── result.ts                 #   Result<T, E> (ok/err helpers)
│       │   ├── guards.ts                 #   isAppError(), isRetryable()
│       │   └── redact.ts                 #   strip secrets/PII from context
│       └── package.json                  #   @acme/errors-core — semver'd
│
├── src/
│   ├── shared/
│   │   ├── registry/
│   │   │   └── error-codes.ts            #   pure data: every public code → metadata
│   │   └── resilience/
│   │       └── retry-policies.ts         #   named policies: stripeHttp, postgresTx,
│   │                                     #   queueJob, llmProvider (+ budgets)
│   ├── features/
│   │   ├── checkout/
│   │   │   ├── errors.ts                 #   CHECKOUT_* (CardDeclined, IdempotencyConflict…)
│   │   │   ├── checkout.service.ts
│   │   │   └── index.ts                  #   public: service + error types ONLY
│   │   ├── export/
│   │   │   ├── errors.ts                 #   EXPORT_* (RowLimitExceeded, SourceUnavailable…)
│   │   │   └── export.job.ts             #   ExportJob workflow (checkpointing)
│   │   ├── webhooks/
│   │   │   └── errors.ts                 #   WEBHOOK_* (SignatureInvalid, EventTooOld…)
│   │   └── agent/
│   │       └── errors.ts                 #   AGENT_* + LLM_* (TokenLimit, InvalidOutput…)
│   ├── infra/
│   │   ├── postgres/errors.ts            #   fromPgError: SQLSTATE table (6 core states)
│   │   ├── stripe/errors.ts              #   fromStripeError: card / rate / unavailable
│   │   ├── s3/errors.ts                  #   fromS3Error: NoSuchKey / SlowDown / network
│   │   ├── redis/errors.ts
│   │   └── llm/errors.ts                 #   fromProviderError (AgentRun provider-agnostic)
│   ├── transports/
│   │   ├── http/
│   │   │   ├── error-handler.ts          #   ONE global catch-all boundary (Express/Nest)
│   │   │   └── serialize-problem.ts      #   ONE RFC 9457 serializer
│   │   ├── jobs/
│   │   │   ├── runner.ts                 #   per-job boundary: retry vs DLQ decision
│   │   │   └── serialize-failure.ts      #   ONE DLQ payload serializer
│   │   └── webhooks/
│   │       └── ack.ts                    #   retryable → 503; permanent → 400; ok → 200
│   └── workflows/
│       └── checkout-saga/
│           ├── steps.ts                  #   Reserve → Charge → Activate
│           └── compensations.ts          #   release-hold, refund — colocated
└── docs/
    └── error-reference.md                #   GENERATED from shared/registry (build step)
```

## Worked example — what each module actually holds

```ts
// packages/errors-core/src/app-error.ts — kernel, zone 1. No product knowledge.
export abstract class AppError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  readonly retryable: boolean = false;
  readonly details?: Record<string, unknown>;
  constructor(message: string, opts?: { cause?: unknown; details?: Record<string, unknown> }) {
    super(message, opts?.cause !== undefined ? { cause: opts.cause } : undefined);
    this.details = opts?.details;
  }
}

// src/features/export/errors.ts — feature-owned, zone 2.
import { AppError } from "@acme/errors-core";

export class ExportRowLimitExceeded extends AppError {
  readonly code = "EXPORT_ROW_LIMIT_EXCEEDED";
  readonly category = "validation" as const;
  constructor(readonly rows: number, readonly limit: number) {
    super(`Export has ${rows} rows; plan limit is ${limit}`);
  }
}

// src/infra/stripe/errors.ts — adapter, zone 3: translate only, never retry.
import { AppError } from "@acme/errors-core";
import { CardDeclinedError } from "../../features/checkout";

export function fromStripeError(err: unknown): AppError {
  if (isStripeCardError(err)) return new CardDeclinedError(err.code, { cause: err });
  if (isStripeRateLimit(err))
    return new DependencyError("DEP_STRIPE_RATE_LIMITED", { retryable: true, cause: err });
  return new DependencyError("DEP_STRIPE_UNAVAILABLE", { retryable: true, cause: err });
}

// src/transports/jobs/runner.ts — job boundary: the retry-vs-DLQ decision, once.
import { RETRY_POLICIES } from "../../shared/resilience/retry-policies";
import { toJobFailure } from "./serialize-failure";

export async function runJob<T>(name: string, fn: () => Promise<T>, ctx: JobCtx) {
  const policy = RETRY_POLICIES.queueJob;
  for (let attempt = 1; attempt <= policy.attempts; attempt++) {
    try { return await fn(); }
    catch (err) {
      const e = toAppError(err);
      if (!policy.retryOn(e) || attempt === policy.attempts) {
        await dlq.publish(name, toJobFailure(e, attempt, ctx.correlationId)); // terminal
        throw e;
      }
      await sleep(backoff(policy, attempt));   // full jitter, centralized
    }
  }
}
```

Dependency direction in this tree: `transports → features/shared/kernel`,
`infra → features + kernel`, `features → kernel`, `shared/registry → nothing`. That is the
entire legal edge set — anything else is a review finding.

## Key data

- **File counts at full size:** 1 kernel package (4 files), 2 shared modules, 4 feature error
  files, 5 adapter translation modules, 5 transport files, 1 saga pair ≈ **22 files** total for
  a product of Acme's breadth. Most products need 8–12.
- **Codes per feature (Acme snapshot):** Checkout 12, Export 8, Webhooks 6, Agent 10, adapters
  9 shared `DEP_*` codes — 45 public codes, 0 in the kernel.
- **Policy inventory:** 4 named retry policies; 1 DLQ serializer; 1 HTTP serializer; 1 global
  HTTP handler; 1 job boundary. The counts of *singleton* modules (serializers, handlers,
  policies) are the invariant to preserve as the tree grows.
- **Generated artifacts:** `docs/error-reference.md` rebuilt from the registry on every merge —
  documentation drift becomes a CI failure, not a support surprise.

## Real-world use case — Acme SaaS

The tree above is the post-refactor state after Acme's god-module migration (see the deep-dive
on god modules). Adoption was incremental: month 1 added `packages/errors-core` and moved
Checkout; month 2 moved Export and the job boundary; month 3 added the registry and generated
docs; month 4 moved AgentRun and the LLM adapter. Each month shipped independently — the tree is
a destination you can walk to, not a flag-day rewrite. The measurable results at month 6: mean
time to locate an error definition (support-driven lookups) fell from ~40 minutes to ~4; retry
constants at call sites: 7 → 0; kernel changes that quarter: 1 (a redaction field addition),
with zero coordinated upgrades required of feature teams.

## Trade-offs

| Project size | Minimum tree | What to skip |
| ------------ | ------------ | ------------ |
| MVP (1–2 devs) | `errors/` flat: kernel file + 1 feature file + 1 transport file | packages/, workflows/, generated docs |
| Startup (3–10 devs) | This tree minus `packages/` (kernel as `src/kernel/`) | Per-vendor retry policies (one generic policy) |
| Scale (multiple teams) | Full tree + CODEOWNERS per module + CI graph rules | Nothing — every slot earns its keep here |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Grow into the slots as each need appears | Create the full tree on day one for a 2-person MVP |
| Keep singleton counts invariant (1 serializer/transport) | Add a second "helper" serializer later |
| Generate the error reference from the registry | Hand-maintain a docs table of codes |
| Point CODEOWNERS at each zone folder | Leave adapters unowned "because infra is shared" |

## Common mistakes

- **Copying the full tree into an MVP.** Twenty-two files for four endpoints breeds unused
  abstractions. Start with three files; the structure tells you *where* things will go.
- **Filling empty slots prematurely.** An empty `workflows/` folder invites a global
  compensation service before a second saga exists. Create slots on demand.
- **Forking the tree per service.** Microservice B copies service A's tree including its
  feature codes. Share only the kernel package; trees are per-repo, codes are per-service.

## Checklist

- [ ] Your repo's error files map one-to-one onto a slot in this tree (or a documented shrink).
- [ ] Singleton modules exist exactly once per transport/policy class.
- [ ] Kernel is a separately versioned package once ≥ 2 deployables exist.
- [ ] Error reference docs are generated, not hand-edited.
- [ ] CODEOWNERS covers every zone folder.

## Related

- [Standard Directory Structure](../01-concepts/05-feature-modules-and-navigability.md)
- [Extracting a Feature-Owned Error Module](./02-extracting-a-feature-owned-error-module.md)
- [Directory Structure Reference](../05-reference/README.md)
