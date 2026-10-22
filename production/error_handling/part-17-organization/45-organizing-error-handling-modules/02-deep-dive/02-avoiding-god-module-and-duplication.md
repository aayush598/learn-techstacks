# Avoiding the God Module and Duplication

> Part XVII · Chapter 45 · Sections 45.13, 45.14 · _Estimated reading time: 14 min_
> **Prerequisite:** [Circular Dependency Avoidance](./01-circular-dependency-avoidance.md)

## In one sentence

The **god module** (one file that imports and knows everything) and **duplication** (the same
translation/policy written in three places) are the same disease at two scales — *policy with
no owner* — and both are cured by extraction with a named owner, not by a new framework.

## Why this matters in production

Both diseases present as "error handling works, until it doesn't":

- **God module symptoms.** `utils/errors.ts` (or its mutant, `shared/errors/index.ts`) passes
  2,000 lines. Every feature imports it, so every feature rebuilds on any change. Merge conflicts
  in that file are near-daily. Nobody can state its public API; everyone is afraid to delete
  anything. A single accidental change to the base class regresses unrelated services — and the
  regression ships because "nobody owns" the file well enough to review deeply.
- **Duplication symptoms.** `23505 → conflict` is mapped in three repositories with three
  different codes. A policy fix (add jitter, respect `Retry-After`) lands in one copy. During a
  provider incident the fixed copy behaves; the three stale copies storm. Duplicated error
  handling is a *correctness* problem disguised as a style problem.

The common root: a decision (what this code means, how this policy behaves) was written down
where no one was assigned to maintain it.

## Core concept: the god module (45.13)

A god module is any error file whose **import fan-in exceeds the number of zones it should
know about**. The kernel knows zero zones; an adapter knows its vendor + kernel; a transport
handler knows registry + kernel + (read-only) domain metadata. A file that knows *all* of them
is a god module regardless of its name or folder.

How god modules actually form — five feeder habits:

1. **The convenience barrel.** `export * from "./checkout"; export * from "./pg"; ...` — one
   import site for everything, one file that couples everything.
2. **The migration "temporary."** "We'll split `errors.ts` after the launch." The launch is
   never over.
3. **The helper accretion.** `formatStripeError`, `toJobPayload`, and `retryWithBackoff` all
   get parked in "the errors file" because it is the first file people open.
4. **The cycle fuse.** Two modules cycle; someone merges them (see circular-deps §fusing).
5. **The utility gravity.** Any file named `utils` or `helpers` is assumed to be a safe import
   target, so cross-zone code flows in by default.

## Core concept: duplication (45.14)

Three kinds of duplication matter, each with its own extraction target:

| Kind | Example | Extract into | Owner |
| ---- | ------- | ------------ | ----- |
| **Translation duplication** | SQLSTATE `23505` mapped in 3 repositories | `infra/postgres/errors.ts` | Postgres adapter |
| **Policy duplication** | retry constants pasted at 5 call sites | `shared/resilience/retry-policies.ts` | Resilience module |
| **Serialization duplication** | error JSON built inline in 8 controllers | `transports/http/serialize-problem.ts` | HTTP boundary |

The extraction test (rule of three, applied): at **three** copies, stop and extract; at two,
leave a `TODO(owner)` comment. Extraction must delete all copies — a "shared" helper that
coexists with the old copies has merely added a fourth thing to maintain.

## How it works (mechanics): unfusing a god module

1. **Freeze it.** Announce: no new exports or helpers in `errors.ts`. New code goes to its zone.
2. **Inventory.** Classify every export into a zone: kernel primitive / feature code / adapter
   mapping / transport serializer / retry policy / misc. "Misc" is always smaller than feared.
3. **Move, don't rewrite.** Relocate each item to its zone file, keeping the old import path as
   a one-release re-export shim with a deprecation comment and removal ticket.
4. **Kill the barrel.** Remove `export *` re-exports; consumers import from the owning module.
5. **Delete the shim.** After one release cycle, delete re-exports; CI (or a failing test on
   the old path) proves stragglers.
6. **Guard.** Add the import-boundary lint rules from circular-deps so the file cannot refill.

The health metric after unfusing: the old file's line count goes to zero within two releases,
and no zone file exceeds its expected fan-in.

## Worked example — before/after extraction

```ts
// BEFORE — utils/errors.ts (god module, excerpt; imports EVERYTHING).
import { Pool } from "pg";
import Stripe from "stripe";
import { REGISTRY } from "../shared/registry";
export * from "../features/checkout/errors";
export * from "../features/export/errors";

export function fromPgError(e: any) { /* 23505 → conflict, inline */ }
export function fromStripeError(e: any) { /* card → declined, inline */ }
export async function withRetry(fn: any, n = 5) { /* inline constants */ }
export function problemJson(e: any, res: any) { /* inline RFC-9457-ish */ }

// AFTER — five owned homes; the god file is gone.
// infra/postgres/errors.ts      → fromPgError()        (adapter owner)
// infra/stripe/errors.ts        → fromStripeError()    (adapter owner)
// shared/resilience/retry-policies.ts → RETRY_POLICIES.queueJob etc.
// transports/http/serialize-problem.ts → toProblemDetails()
// features/checkout/errors.ts, features/export/errors.ts → codes, feature-owned
```

For duplication, the same shape: three inline `23505` checks become one exported branch in
`fromPgError`, and the three call sites call it. The policy fix then lands once, and every
caller inherits it on the next deploy.

## Key data

- **Fan-in guardrails (practical thresholds):** kernel ≤ 0 internal imports; feature `errors.ts`
  ≤ 1 internal import (kernel); adapter ≈ 2 (kernel + its feature codes); transport handler ≤ 3
  (kernel, registry, serializer). A file at 8+ internal imports is a god-module candidate.
- **File size guardrails:** error files above ~300 lines or ~20 codes deserve a split review.
  The longest healthy grouped `errors.ts` observed at Acme scale: 14 codes / 96 lines.
- **Shim lifetime:** one release (or at most two) between re-export and deletion; longer shims
  become the new permanent coupling.
- **Conflict rate proxy:** god modules show up in git as the top-5 most conflicted files per
  quarter; that ranking is a free diagnostic — if `errors.ts` is on it, it is a god module.

## Real-world use case — Acme SaaS

Acme's `shared/errors/index.ts` had grown to 1,840 lines spanning Checkout, ExportJob,
WebhookIngest, and AgentRun codes plus `withRetry` and two serializers. Two incidents in one
quarter traced to it: (1) an AgentRun PR changed the shared `AppError.message` formatting,
silently altering every consumer's DLQ payload; (2) a Checkout hotfix to decline-handling
rebuilt the worker bundle, delaying an unrelated export release by half a day. The unfusing
relocated 46 exports into 9 zone-owned files; the barrel was deleted at release N+1. Post-move,
the top conflicted file list no longer contained any error module, and the median CI build for
feature-only PRs dropped because feature PRs no longer rebuilt the world. The team also
committed to the "3 copies → extract" rule for translations, which retired two ad-hoc retry
helpers in the same quarter.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Zone extraction with shims (recommended) | Preserves history; safe rollout; clear owners | Temporary duplicate paths during shim window | Any god module in active use |
| Big-bang rewrite into zones | Clean immediately | High regression risk; unreviewable PR | Dead or toy code only |
| Leave god module, add docs | Zero migration cost | Diseases continue; conflicts and blast radius grow | Never for production |
| Extract at 2 copies preemptively | Minimal duplication ever | Abstraction noise before pattern is proven | Only for vendor adapters (cheap, stable) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Freeze the god module before extracting | Keep accepting "just one more helper" |
| Delete every copy when you extract | Add a shared helper *beside* the originals |
| Give each extracted file an owner in CODEOWNERS | Extract into another unowned shared folder |
| Treat top-conflicted-files as a god-module signal | Wait for a production incident to split it |

## Common mistakes

- **Extraction without deletion.** The shared helper is added; old copies "for compatibility"
  remain. Now there are two sources of truth — worse than one. Delete, and fix callers.
- **God module reborn as a folder.** Moving everything into `errors/` with 12 files but one
  barrel `index.ts` that re-exports all — the coupling persists at folder scale. Do not rebuild
  the barrel.
- **Extracting policy into the kernel.** `withRetry` moves from the god file into the kernel
  "because everyone uses it." Retry policy is not a primitive; it belongs in the resilience
  module (see supporting modules 45.9).
- **No owner after extraction.** An unowned folder of nine files is a slower god module. Every
  extracted file gets a named owner team before the PR merges.

## Checklist

- [ ] No error file has internal import fan-in above its zone's threshold.
- [ ] Any policy/translation found at 3+ sites has exactly one shared definition, and the copies
      are deleted.
- [ ] God-module migrations include a shim removal ticket with a date.
- [ ] CODEOWNERS (or equivalent) lists an owner for every extracted module.
- [ ] Top-conflicted-files report reviewed quarterly for `errors`-named files.

## Related

- [Circular Dependency Avoidance](./01-circular-dependency-avoidance.md)
- [Shared Kernel vs App-Specific Code](../01-concepts/02-shared-kernel-vs-app-specific.md)
- [Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
