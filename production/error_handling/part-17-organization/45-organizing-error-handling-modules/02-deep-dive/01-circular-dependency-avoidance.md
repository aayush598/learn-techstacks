# Circular Dependency Avoidance in Error Modules

> Part XVII · Chapter 45 · Section 45.12 · _Estimated reading time: 15 min_
> **Prerequisite:** [The Four Zones](../01-concepts/03-core-zones-primitives-domain-infra-transport.md)

## In one sentence

Error modules cycle when a *shared* module (registry, kernel, shared helpers) needs to know
about *specific* modules (features, vendors, transports) — so the fix is always the same shape:
**push the specific knowledge down as data or invert the dependency with an interface owned by
the lower layer.**

## Why this matters in production

Circular dependencies between error modules do not fail loudly at first. They fail as:

- **Load-order bugs.** In Node/TS, a cycle means one module is observed half-initialized:
  `REGISTRY` is `undefined` inside a function that runs at import time, and the failure appears
  only in production builds with different bundling than dev.
- **The god-module collapse.** Teams "fix" the cycle by merging the two modules into one file
  that imports everything. That file becomes 45.13's god module — the cycle didn't disappear,
  it was fused.
- **Un-replaceable vendors.** A cycle between `kernel` and `infra/stripe` means Stripe types
  are load-bearing for the whole app; swapping or mocking the provider for tests requires
  loading the kernel with vendor mocks.

Cycles are therefore an *architectural* failure mode with runtime symptoms — which is why they
must be caught at the import-graph level, not the stack-trace level.

## The four classic error-module cycles

```text
CYCLE A — Registry ↔ Transport
  error-codes.ts imports statusFor() from http/   (needs behavior)
  http/error-handler.ts imports REGISTRY           (needs data)
  FIX: registry is pure data; status lookup is a kernel helper reading the data.

CYCLE B — Kernel ↔ Feature
  kernel/app-error.ts imports CheckoutError        (kernel wants "all types" guard)
  checkout/errors.ts imports AppError              (needs base class)
  FIX: kernel defines structural guard isAppError(); feature types register nothing.

CYCLE C — Domain ↔ Adapter
  checkout/service.ts imports fromPgError          (wants translation "for convenience")
  infra/postgres/errors.ts imports ConflictError   (needs domain code to produce)
  FIX: domain defines ConflictError; adapter depends on domain (one-way). Domain
       never calls the adapter's mapper; composition root wires them.

CYCLE D — Retry module ↔ Classification
  retry-policies.ts imports fromStripeError        (needs to classify before retrying)
  stripe adapter imports RETRY_POLICIES            (adapter "auto-retries")
  FIX: adapters translate only; retry module reads metadata (e.retryable);
       the caller (job runner / client wrapper) owns the loop.
```

## How it works (mechanics): the four break techniques

1. **Pure data.** Anything both sides need to *read* becomes data with no imports (the registry
   pattern). Data has no dependency direction problem.
2. **Structural guards, not nominal imports.** The kernel answers "is this an AppError?" with a
   type guard over fields (`code`, `category`), not by importing every subclass.
3. **Depend on the domain, not on the caller.** Adapters may import feature error *types*
   (they translate toward the domain). The reverse edge — domain importing adapters — is the
   one to delete; wire the adapter at the composition root (DI or direct call in the service's
   constructor, injected from `app.ts`).
4. **Metadata over callbacks.** Retry and serialization modules branch on *fields* the error
   already carries (`retryable`, `httpStatus`), never on callbacks or instanceof chains that
   reach into other modules.

**Detection.** Make cycles impossible to merge:

```yaml
# dependency-cruiser config (excerpt) — enforce one-way zones in CI
forbidden:
  - name: domain-must-not-import-infra
    from: { path: "^src/features/" }
    to:   { path: "^src/infra/" }
  - name: kernel-must-not-import-anything-internal
    from: { path: "^src/kernel/" }
    to:   { path: "^src/(features|infra|transports|workflows)/" }
  - name: no-circular
    from: {} to: { circular: true }
```

Run it in CI. An import-graph rule catches the cycle in the PR; a runtime crash catches it in
production.

## Worked example — breaking Cycle A

```ts
// BEFORE — cycle. registry needs behavior; http needs data.
// shared/registry/error-codes.ts
import { statusFor } from "../../transports/http/status";   // ← wrong direction
export const REGISTRY = { PROJECT_SLUG_TAKEN: { status: statusFor("conflict") } };

// transports/http/error-handler.ts
import { REGISTRY } from "../../shared/registry/error-codes";

// AFTER — registry is pure data; the lookup helper lives in the kernel.
// kernel/registry-lookup.ts
export function statusFor(code: string, fallback = 500): number {
  return REGISTRY[code]?.httpStatus ?? fallback;   // REGISTRY injected or imported (data-only)
}

// shared/registry/error-codes.ts — imports nothing.
export const REGISTRY = {
  PROJECT_SLUG_TAKEN: { httpStatus: 409, retryable: false, publicTitle: "Slug already in use" },
} as const;

// transports/http/error-handler.ts — one-way edge: http → registry (data).
import { REGISTRY } from "../../shared/registry/error-codes";
```

The import graph becomes `http → registry` and `http → kernel` — a DAG. The registry can now be
consumed by the docs pipeline and the SDK generator without either importing HTTP.

## Key data

- **Edge directions allowed:** transport → domain/kernel/registry; infra adapter → domain/
  kernel; domain → kernel; registry → (nothing). Four legal edge classes cover the whole tree.
- **Where cycles show up in real repos:** the registry↔transport pair (Cycle A) and the
  adapter↔retry pair (Cycle D) account for the large majority of observed error-module cycles;
  kernel↔feature (Cycle B) is rarer but the most expensive to unfuse because it poisons every
  import of the base class.
- **CI cost:** a dependency-cruiser (or eslint boundary) rule over ~1k modules typically runs in
  seconds and catches all static cycles — far cheaper than debugging a half-initialized module
  in a production bundle.

## Real-world use case — Acme SaaS

Acme's `ExportJob` runner originally imported `fromPgError` and `fromStripeError` directly to
classify failures before deciding retry-vs-DLQ — creating Cycle D: the adapters imported
`RETRY_POLICIES` to "helpfully" auto-retry inside the translation function. Symptom: a single
serialization failure (`40001`) triggered retries at **two** nested layers (adapter × job
runner), multiplying attempts 3 × 5 = up to 15 database hits under contention, and the final
error surfaced as `PG_UNEXPECTED` because the outer layer's translation re-wrapped the adapter's
already-translated error. The refactor: adapters translate-only (attach `retryable`), the job
runner reads metadata and applies `queueJob` policy once. Nested-retry amplification disappeared,
and the DLQ payload started carrying the original stable code instead of a re-wrapped one.

## Trade-offs

| Technique | Pros | Cons | When to use |
|-----------|------|------|-------------|
| Pure data (registry) | Trivially shareable; codegen-friendly | No behavior allowed; discipline required | Any shared catalog |
| Structural type guards | Kernel stays independent of features | Slightly weaker typing than nominal instanceof | Cross-module guards |
| Composition-root wiring | True one-way deps; testable | Slightly more setup code | Domain↔adapter edges |
| Metadata-driven policy | Policy modules stay vendor-blind | Metadata fields must be maintained | Retry, serialization |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce zone imports with a CI graph rule | Trust code review alone to spot cycles |
| Make shared catalogs pure data | Add lookup *functions* that import transports |
| Inject adapters at the composition root | Let domain services import adapter mappers |
| Break cycles by inverting, not merging | Fuse two modules into one bigger module |

## Common mistakes

- **"It's just one import."** The first cross-zone edge is always justified locally and is
  exactly how Cycle B starts. Budget zero tolerated violations; add an eslint-disable only with
  a linked removal ticket.
- **Fusing to fix.** Merging registry + handler removes the cycle symbol and creates the god
  module. If your fix increases a file's import fan-in, it is the wrong fix.
- **Runtime registry mutation.** `registry.register(code, entry)` called from feature modules at
  import time recreates the cycle dynamically and adds load-order fragility. Keep the registry
  static; add codes by editing data (or codegen from feature annotations in build).

## Checklist

- [ ] CI fails the build on any circular import among error modules.
- [ ] The registry file imports nothing.
- [ ] No domain file imports `infra/**` (enforced, not assumed).
- [ ] Retry/serialization decisions read metadata fields, not foreign classes.
- [ ] Composition root is the only place that wires adapters into services.

## Related

- [Where Error-Handling Code Belongs](../01-concepts/01-where-error-code-belongs.md)
- [Avoiding a Global God Module and Duplication](./02-avoiding-god-module-and-duplication.md)
- [Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
