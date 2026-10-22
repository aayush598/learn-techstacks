# Extracting a Feature-Owned Error Module — Before/After

> Part XVII · Chapter 45 · Sections 45.16, 45.17 (applied) · _Estimated reading time: 16 min_
> **Prerequisite:** [Acme SaaS Error Module Tree](./01-acme-error-module-tree.md)

## In one sentence

This walkthrough takes Checkout's errors out of a global shared file and into a feature-owned
module — the single most common refactoring in this chapter — with the exact before code, the
extraction steps, the after code, and the migration tactics that keep both old and new import
paths working during the transition.

## Why this matters in production

Checkout is where money moves, so its errors are edited under incident pressure more often than
any others. While they lived in `shared/errors/index.ts`, every Checkout error change:

- triggered CI for Export, Webhooks, and AgentRun (shared barrel fan-out),
- required reviews from teams that did not own payments,
- risked unrelated bundles regressing (worker rebuilds on shared-package changes),
- and made "who deprecates `CHECKOUT_CARD_DECLINED`?" a meeting instead of a CODEOWNERS lookup.

The extraction converts an org-wide event into a one-team PR. The pattern is identical for every
other feature — ExportJob, WebhookIngest, AgentRun — so learn it once here.

## Before: the shared catalog

```ts
// shared/errors/index.ts — the global file (excerpt). EVERYTHING imports this.
import { AppError } from "../../packages/errors-core";

// …27 other codes live here, across four features…

export class CardDeclinedError extends AppError {
  readonly code = "CHECKOUT_CARD_DECLINED";
  readonly category = "conflict" as const;   // ← wrong category, inherited by copy-paste
  override readonly retryable = false;
  constructor(readonly reason: string) { super(`Card declined: ${reason}`); }
}

export class IdempotencyKeyConflict extends AppError {
  readonly code = "CHECKOUT_IDEMPOTENCY_CONFLICT";
  readonly category = "conflict" as const;
  override readonly retryable = false;
  constructor() { super("Idempotency key reused with different payload"); }
}

// …helper drift: only SOME codes get an httpStatus field; the HTTP handler
// has a second, hand-maintained switch for the ones that don't…
export function isCheckoutError(e: unknown): e is CardDeclinedError | IdempotencyKeyConflict {
  return e instanceof AppError && e.code.startsWith("CHECKOUT_");
}
```

Problems visible in this excerpt, all of which the extraction fixes:

1. **Ownership gap.** No module owns `CHECKOUT_*`; the file's "owner" is whoever merges first.
2. **Metadata drift.** `CardDeclinedError` has the wrong category (`conflict` instead of a
  payment/business category) because it was cloned from a slug-uniqueness error — nobody with
  Checkout context reviewed it.
3. **Duplicated routing logic.** `isCheckoutError` re-implements prefix logic that the registry
   should provide once.

## The extraction steps

1. Create `features/checkout/errors.ts` with the Checkout codes only (keep the kernel base).
2. Move classes verbatim first — fix the category drift in a *separate* PR so the move's diff
   stays reviewable and behavior-preserving.
3. Point `features/checkout/checkout.service.ts` at the new module.
4. Leave `shared/errors/index.ts` re-exporting the moved symbols for one release, marked
   deprecated with the owning PR link.
5. Update remaining importers feature-by-feature; CI greps for the old path.
6. Delete the re-exports and `isCheckoutError` (the registry/prefix convention replaces it).

## After: feature-owned module

```ts
// features/checkout/errors.ts — owned by the Checkout team (CODEOWNERS).
import { AppError } from "@acme/errors-core";

/** Payment was declined by the issuer/gateway. Non-retryable with the same card. */
export class CardDeclinedError extends AppError {
  readonly code = "CHECKOUT_CARD_DECLINED" as const;
  readonly category = "business_rule" as const;   // fixed with Checkout context
  override readonly retryable = false;
  constructor(readonly declineReason: string, opts?: { cause?: unknown }) {
    super("Payment card was declined", opts);
  }
}

/** Same idempotency key, different payload — caller bug, HTTP 409/422 per contract. */
export class IdempotencyKeyConflict extends AppError {
  readonly code = "CHECKOUT_IDEMPOTENCY_CONFLICT" as const;
  readonly category = "conflict" as const;
  override readonly retryable = false;
  constructor(opts?: { cause?: unknown }) {
    super("Idempotency key reused with a different request payload", opts);
  }
}

export type CheckoutError = CardDeclinedError | IdempotencyKeyConflict;

// features/checkout/index.ts — the ONLY public surface.
export * from "./checkout.service";
export { CardDeclinedError, IdempotencyKeyConflict } from "./errors";
export type { CheckoutError } from "./errors";

// shared/registry/error-codes.ts — entries added in the SAME PR as the move
// (registry discipline: a code without an entry fails CI).
CHECKOUT_CARD_DECLINED:            { httpStatus: 402, retryable: false, publicTitle: "Card declined" },
CHECKOUT_IDEMPOTENCY_CONFLICT:     { httpStatus: 409, retryable: false, publicTitle: "Idempotency conflict" },
```

The service now imports from its own folder; the transport reads metadata off the error; the
registry — not a hand-written switch — picks the HTTP status. A new Checkout code touches
exactly two files (`features/checkout/errors.ts` and the registry entry), both owned by one
team.

## Key data

- **Diff shape of the extraction PR (Acme actuals):** +118 / −64 across 9 files; review time
  same-day; zero Export/AgentRun changes required (their CI still ran — that is the point of
  the shim window).
- **Files touched per new Checkout code after extraction:** 2 (definition + registry), down
  from 4–5 (global file, registry, handler switch, docs table, sometimes barrel).
- **Shim window:** one release (~2 weeks at Acme's cadence). Two release trains later, the old
  import path was gone; `grep -r "shared/errors"` returned zero feature imports.
- **Category-drift correction:** `CardDeclinedError` moved from `conflict` to `business_rule`;
  any consumer that had branched on `category === "conflict"` for this code was found by
  compiling with the union type and fixed in the same series.

## Migration tactics that keep the lights on

| Tactic | Why it works |
| ------ | ------------ |
| **Move first, fix second** | Behavior-preserving moves are reviewable; semantic fixes ride their own PRs |
| **One-release re-export shim** | No big-bang caller updates; old path fails CI once the shim is deleted |
| **Registry entry in the same PR** | Prevents the classic half-migration: moved class, missing metadata |
| **Union type per feature** | `CheckoutError` gives callers exhaustiveness without a global registry import |
| **CI grep for the old path** | Makes stragglers visible before shim deletion, not after |

## Real-world use case — Acme SaaS

Acme extracted `EXPORT_*` codes for `ExportJob` using this exact sequence. Mid-migration, an
incident hit: an export of a large workspace failed with `EXPORT_ROW_LIMIT_EXCEEDED`, and two
on-call engineers searched the old global file for ten minutes before finding the class had
already moved. Post-incident action: the shim carried a JSDoc `@deprecated moved to
features/export/errors.ts` tag, and the runbook's first step became "grep the new location."
Subsequent extractions (WebhookIngest, AgentRun) had zero mid-incident confusion because the
on-call rotation's runbook entry now named the feature-folder convention explicitly — evidence
that **navigability conventions are part of the incident-response tooling**, not just aesthetics.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Incremental with shim (recommended) | Safe; reviewable; no flag day | Temporary dual paths | Any live product |
| Big-bang move of all features | One PR; no shims | Unreviewable; high regression risk | Pre-launch repos only |
| Copy codes to feature, leave originals | Zero breakage during move | Permanent duplication (anti-pattern 46.20's cousin) | Never |
| Leave shared file, add owners only | Cheapest | Metadata drift and fan-out remain | Only if code freeze imminent |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Add the registry entry in the extraction PR | Move classes and "do the registry later" |
| Keep the move PR behavior-only | Mix refactors with category/logic fixes |
| Delete the shim on a scheduled date | Let deprecation shims live forever |
| Export a per-feature error union type | Force consumers to import the kernel for guards |

## Common mistakes

- **Shim infinity.** The deprecated re-export becomes load-bearing because one internal tool
  still imports it. Set the deletion date at extraction time and make CI enforce it.
- **Moving without CODEOWNERS.** The folder exists but ownership was never assigned; the next
  team re-shares it. Ownership is part of the extraction definition of done.
- **Registry lag.** Class moved, registry entry missing → transport falls back to 500 for a
  402-class error. The same-PR rule exists because this failure is silent in tests that mock
  the transport.

## Checklist

- [ ] Feature `errors.ts` contains all codes with the feature's prefix — and only those.
- [ ] Registry entries exist for every moved code in the same PR.
- [ ] CODEOWNERS names the owning team for the new folder.
- [ ] Shim has a dated deletion ticket and a CI grep guarding it.
- [ ] Per-feature error union type exported for caller exhaustiveness.

## Related

- [Acme SaaS Error Module Tree](./01-acme-error-module-tree.md)
- [Avoiding a Global God Module and Duplication](../02-deep-dive/02-avoiding-god-module-and-duplication.md)
- [Where Error-Handling Code Belongs](../01-concepts/01-where-error-code-belongs.md)
