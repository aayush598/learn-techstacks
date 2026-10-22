# Avoiding Tight Coupling and the Giant Error Module

> Part IV · Chapter 10 · Sections 10.12, 10.13 · _Estimated reading time: 19 min_
> **Prerequisite:** [The Machinery of Centralized Handling](../01-concepts/02-the-machinery-of-centralized-handling.md)

## In one sentence

Centralization fails when the shared error machinery **imports the whole application** (tight
coupling, 10.12) or grows into a **single god module** nobody can change (10.13) — the fix is
dependency inversion: the center depends on a small registry, and features register into it.

## Why this matters in production

The trajectory is painfully common:

1. Week 1: `errors.ts` with ten codes. Fine.
2. Month 3: every feature imports `errors.ts`; `errors.ts` starts importing feature types to
   build context fields. Circular import warnings appear.
3. Month 9: `errors.ts` is 1 200 lines, touched by every PR, owned by nobody. Teams work around
   it with local `throw new Error(...)` — and centralization dies exactly where you needed it.

This is not a style problem: coupling makes each error change a cross-team negotiation, and the
god module becomes the thing that *prevents* consistent handling rather than providing it.

## Core concept — dependency direction

The center must depend on **abstractions owned by nobody and everybody**: the error type, the
code registry interface, the serializer. Features depend on the center. Never the reverse.

```text
 ❌ COUPLED                                   ✅ INVERTED
 feature ──▶ errors.ts ──▶ feature types      feature ──▶ error-kernel (type + registry API)
                                    ▲                    ▲
                                    └── cycle             └── kernel imports NOTHING from features
                                                          kernel ← registration done BY features
```

Three structural rules:

1. **Kernel purity.** The shared kernel contains: `AppError` type, registry interface,
   `normalize()`, `toProblem()`, redaction, status maps derived from the registry. It imports
   zero domain/infra packages.
2. **Feature-owned registration.** `billing` declares and registers `INVOICE_FINALIZED` in its
   own module; the registry collects registrations. The center maps *codes*, never *types*.
3. **No context fields in the kernel.** Per-feature metadata rides as a generic, redacted
   `meta` record validated by the feature, not by the kernel.

```ts
// kernel — no feature imports, ever
export interface ErrorCodeSpec {
  code: string;                 // "BILLING_INVOICE_FINALIZED"
  status: number;               // 409
  retryable: boolean;
  title: string;
  public: boolean;              // may appear in external responses
}
export const registry = createRegistry<ErrorCodeSpec>();  // features call registry.register()

// feature/billing/errors.ts — ownership stays local
registry.register({ code: "BILLING_INVOICE_FINALIZED", status: 409, retryable: false,
                    title: "Invoice is finalized", public: true });
```

## The god module (10.13) — symptoms and the split

| Symptom | What it means | Split |
| ------- | ------------- | ----- |
| Kernel file > ~300 lines of codes | codes are feature-owned | move declarations into feature modules |
| Kernel imports any `*/domain/*` | inversion violated | delete the import; add a registry entry |
| Every PR touches the kernel | merge contention | registration-at-startup pattern |
| Teams add `Error2`, `ErrorAlt` | bypasses created | make the correct path the easy path |
| Tests of one feature need the whole app | hidden coupling | kernel tests are pure; feature tests register locally |

**The split in practice:** keep the kernel at three files — `types.ts`, `registry.ts`,
`serialize.ts`. Everything else moves to `features/<name>/errors.ts`. The central *policy*
(serializer, redaction, status derivation) stays central; the *data* (which codes exist) becomes
distributed. That is the difference between a shared library and a god module.

## Key data / numbers

- A healthy kernel budget (recommendation): **≤ 300 lines**, **0 feature imports**, **≤ 3 public
  entry points** (`register`, `normalize`, `toProblem`).
- Registry size heuristic: codes should scale with *domains* (~5–20 per domain), not with *PRs*;
  a registry growing faster than features is accumulating duplicates (Chapter 8 governance).
- Lint enforcement: `no-restricted-imports` / dependency-cruiser rule — `kernel/**` may not
  import `features/**` or `infra/**`. Make the direction a CI error, not a convention.
- Duplicate-code detection: a CI check fails when two registrations claim the same `code` string
  (globally unique across the monorepo).

## Real-world use case — Acme SaaS

Acme's `core/errors/index.ts` grew to 1 400 lines and imported the `Workspace` domain type to
type a `meta.workspaceId` field. Consequences: circular imports forced lazy `require`s; two
teams shipped `BILLING_ERROR_2` and `BILLING_ERROR_V2` to avoid the review queue; the serializer
accidentally exposed a Stripe field because "the kernel knows about Stripe now."

The refactor: kernel shrank to 180 lines (types, registry, serializer); each feature registered
its own codes; `meta` became `Record<string, unknown>` validated per-feature; an import-boundary
lint rule locked the direction. The duplicate codes were deprecated via the registry's
deprecation table (Chapter 8), and PRs touching the kernel dropped from ~daily to ~monthly.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Thin kernel + feature registration (recommended) | No cycles, parallel ownership | Registration ceremony; needs startup wiring | Any codebase > ~5 modules |
| Central code list in one file | Genuinely simple at small size | Becomes the god module by accretion | MVP only, with a scheduled split |
| Full per-module error packages, no kernel | Maximum ownership | Envelope drift; serializer duplication | Multi-repo setups with a published contract package |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the kernel free of feature imports | Import domain types "just for typing" |
| Let features register their own codes | Maintain one giant switch of all codes |
| Enforce dependency direction in CI | Trust good intentions |
| Deprecate codes via the registry | Add `Foo2` to dodge review |

## Common mistakes

- **Registration order bugs** — codes missing at runtime because a module was never imported;
  register at explicit startup wiring (bootstrap layer, Ch. 9) and assert total registration in
  tests.
- **Kernel growing "small helpers"** — `formatMoney()` in the kernel is a domain concern; reject
  it in review.
- **Splitting too late** — the cost of the split grows with every feature; schedule it when the
  second domain appears, not the fifth team.

## Checklist

- [ ] Kernel imports zero feature/infra modules (lint-enforced).
- [ ] Each feature owns and registers its codes next to its logic.
- [ ] Duplicate code strings fail CI.
- [ ] Serializer/redaction live only in the kernel and are pure.

## Related

- [Limits of the Global Handler](../01-concepts/03-limits-of-a-global-handler.md)
- [Error Contracts Across Modules and Services](../01-concepts/04-contracts-across-modules-and-services.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
