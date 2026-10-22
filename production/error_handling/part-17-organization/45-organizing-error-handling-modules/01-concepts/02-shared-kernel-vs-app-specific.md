# Shared Kernel vs App-Specific Error Code

> Part XVII · Chapter 45 · Sections 45.2, 45.15, 45.18 · _Estimated reading time: 15 min_
> **Prerequisite:** [Where Error-Handling Code Belongs](./01-where-error-code-belongs.md)

## In one sentence

The **shared kernel** holds only error *primitives* that every module depends on — base class,
result type, category enum, redaction helpers — while every *policy and code* stays in the
feature or adapter module that owns it, because a kernel that grows policy becomes a god module
with a package name.

## Why this matters in production

Two opposite failures dominate real codebases:

- **Fat kernel.** Someone adds `PAYMENT_CARD_DECLINED`, an HTTP map, and a Stripe retry policy
  into `@acme/errors-core`. Now every service — including the ones with no payments — depends on
  payment semantics. A "harmless" kernel change bumps semver for 12 packages, and teams start
  vendoring copies. The kernel becomes the most-coupled module in the system while being sold as
  the least.
- **No kernel.** Each feature defines its own `AppError` base, its own result wrapper, its own
  correlation-id field. The HTTP boundary then needs 8 adapters to serialize 8 shapes, and the
  observability pipeline needs 8 parsers. Consistency — the whole point of an error standard —
  never materializes.

The kernel/app split is how you get consistency *without* coupling.

## Core concept: what earns a place in the kernel

A type belongs in the shared kernel only if **all three** hold:

1. **No domain meaning.** `AppError` yes; `SubscriptionPastDueError` no.
2. **Near-zero change rate.** Kernel changes should be rare, major-version events. If you edited
   it twice this month, it is not a kernel.
3. **Used by ≥ 3 independent modules.** One user means it belongs to that user's module; two
   means wait; three means extract.

```text
┌─────────────────── @acme/errors-core (kernel) ───────────────────┐
│  AppError base · Result<T,E> · ErrorCategory enum                │
│  redact() · CorrelationContext · isAppError() type guard         │
│  (NO codes, NO http maps, NO retry policy, NO vendor types)      │
└───────────────────────────────────────────────────────────────────┘
        ▲                ▲                    ▲
        │ imports        │ imports            │ imports
 ┌──────┴─────┐   ┌──────┴──────┐    ┌────────┴────────┐
 │ checkout/  │   │ export/     │    │ infra/stripe/   │
 │ errors.ts  │   │ errors.ts   │    │ errors.ts       │
 │ (app-      │   │ (app-       │    │ (adapter:       │
│  specific)  │   │  specific)  │    │  translation)   │
 └────────────┘   └─────────────┘    └─────────────────┘
```

## How it works (mechanics)

**Step 1 — Seed the kernel minimally.** Start with a base error carrying `code`, `category`,
`retryable`, `cause`, and `context`; a `Result` type if your language uses one; a redaction
helper. That is roughly 100–200 lines.

**Step 2 — Feature modules own their codes.** `checkout/errors.ts` extends the base, defines
domain codes, and attaches feature metadata (HTTP status is fine as *metadata* on the code —
the transport reads it; the domain never branches on it).

**Step 3 — Adapters own translation.** Vendor types (`StripeError`, `PgError`) are imported
only by the adapter. The adapter converts vendor → kernel/feature types and attaches the vendor
payload as `cause` — never as the thrown type.

**Step 4 — Promote with evidence.** When a third module needs something currently private to
another module (say a `TransientDependencyError` used by both the Stripe and S3 adapters),
promote *that one thing* into the kernel or a sibling shared module — and write the promotion
rule into the kernel's README so future extractions are boring.

## Worked example

```ts
// packages/errors-core/src/app-error.ts — the kernel. Zero product knowledge.
export type ErrorCategory =
  | "validation" | "auth" | "permission" | "not_found" | "conflict"
  | "rate_limit" | "dependency" | "internal";

export abstract class AppError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  readonly retryable: boolean = false;
  readonly details?: Record<string, unknown>;
  constructor(message: string, opts?: { cause?: unknown; details?: Record<string, unknown> }) {
    super(message, opts?.cause ? { cause: opts.cause } : undefined);
    this.details = opts?.details;
  }
}

// src/features/export/errors.ts — app-specific. Kernel never sees these codes.
import { AppError } from "@acme/errors-core";

export class ExportRowLimitExceeded extends AppError {
  readonly code = "EXPORT_ROW_LIMIT_EXCEEDED";
  readonly category = "validation" as const;
  override readonly retryable = false;
  constructor(readonly rows: number, readonly limit: number) {
    super(`Export has ${rows} rows; plan limit is ${limit}`);
  }
}
```

The kernel gained **zero** lines when Export shipped a new error. That is the health metric.

## Key data

- **Kernel size target:** 100–300 lines of primitives for a typical SaaS. Kernels that pass
  ~500 lines or contain any `code = "..."` string are almost certainly accumulating policy.
- **Promotion threshold:** 3+ consuming modules (the "rule of three" applied to error infra).
- **Semver cost:** a breaking kernel change forces coordinated upgrades across every feature
  package; keeping the kernel boring converts weekly release-train pain into quarterly events.
- **Acme's split after 18 months:** kernel 180 lines; 7 feature error modules (12–60 lines each);
  5 adapter translation modules. Zero codes in the kernel.

## Real-world use case — Acme SaaS

Acme's first attempt put the full error catalog — 43 codes with HTTP maps — in a shared
`@acme/acme-errors` package. Six months later, the AgentRun team needed `LLM_TOKEN_LIMIT_EXCEEDED`
added; the change touched the shared package, triggering rebuilds of the API, workers, and CLI,
and a minor-version bump for everyone. Meanwhile the ExportJob team, blocked on the release
train, copy-pasted three codes locally. The fix: shrink the shared package to primitives
(kernel), move codes into `features/*/errors.ts`, and leave the HTTP map as *metadata* read by
the transport. Result: shipping a new feature error stopped being a cross-team event — AgentRun
went from "merge shared package + 3 dependents" (~2 days) to "one PR in one feature folder"
(same-day).

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Minimal kernel + feature-owned codes (recommended) | Low coupling, fast feature velocity, stable semver | Requires discipline at the promotion gate | Any product with ≥ 2 teams or ≥ 2 services |
| Fat shared catalog package | One place to look; uniform codes fast | Cross-team release coupling; unowned codes; vendor creep | Demos, prototypes |
| No kernel; per-feature primitives | Zero coordination cost | N boundary adapters; inconsistent shapes; duplicated redaction | Single-file scripts |

## Over-complex shared abstractions (45.15)

The kernel is where abstraction overreach happens: generic error pipelines, middleware metaclass
registries, decorator-based automatic retry. **A shared abstraction must pay rent**: used
verbatim (no per-call configuration) by ≥ 3 modules *and* save more lines than it adds. If callers
must learn a DSL to use it, it is a framework, not a primitive — and this book's end goal is a
standard, not a framework. Concrete guardrails:

- No abstract classes with more than ~5 overridable members.
- No reflection/decorator magic required to get correct default behavior.
- Every kernel export must be usable in a 5-line test without the rest of the kernel.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep codes, HTTP maps, and retry policy out of the kernel | Add "just this one code" to the shared package |
| Promote with the rule of three | Extract on first use "for consistency" |
| Version the kernel with explicit breaking-change notes | Let features vendor private copies silently |
| Give every kernel export a 5-line usage example | Ship a DSL that must be learned to throw an error |

## Common mistakes

- **Kernel imports a feature "just for one type".** Now the kernel → feature edge exists and the
  cycle begins (see [circular deps](../02-deep-dive/01-circular-dependency-avoidance.md)).
- **Kitchen-sink `helpers`.** `errors-core/helpers.ts` accumulates `formatStripeError` — vendor
  knowledge in the kernel. Vendor helpers live in the vendor's adapter.
- **Silent forks.** A team copies kernel code to move faster; two years later there are three
  incompatible `AppError` bases. Make promotion cheap so forking is unnecessary.

## Checklist

- [ ] The kernel contains no string literal matching `^[A-Z][A-Z0-9_]+$` error codes.
- [ ] The kernel imports nothing from feature, infra, or transport modules.
- [ ] Every feature/adapter error extends the kernel base (or uses the kernel result type).
- [ ] Promotion of private code into the kernel requires 3 evidenced consumers.
- [ ] Kernel changes this quarter: number and reason recorded.

## Related

- [Where Error-Handling Code Belongs](./01-where-error-code-belongs.md)
- [Core Zones: Primitives, Domain, Infra, Transport](./03-core-zones-primitives-domain-infra-transport.md)
- [Avoiding a Global God Module](../02-deep-dive/02-avoiding-god-module-and-duplication.md)
- [Reusable Error-Handling Infrastructure](../../../part-21-maintainability/54-reusable-error-handling-infrastructure/README.md)
