# Versioning Shared Packages Without Breaking Consumers

> Part XXI · Chapter 54 · Sections 54.16, 54.17 · _Estimated reading time: 22 min_
> **Prerequisite:** [The Reusable Core Library](../01-concepts/01-the-reusable-core-library.md), [Chapter 49 — Error Contract Design and Versioning](../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)

## In one sentence

A shared error package's version number is a promise about **blast radius**, and the
classification of a change into additive, behaviour-changing, or breaking determines whether
consumers must do anything.

## Why this matters in production

A package version bump is a *deployment event across every consumer*. If the version number
does not reliably mean "nothing you rely on changed", then every bump triggers a
coordinated migration, and the package becomes a coordination tax rather than an
accelerator.

The specific failure in error packages: **an additive change that is not behaviourally
additive.** Adding a new error code looks harmless, but if the code's *category* maps to a
status the consumers were not expecting, or if a shared table's default changes, the
"additive" release silently changes what existing services return.

## Core concept

### 54.16 — Versioning packages

The version scheme is semver — `MAJOR.MINOR.PATCH` — but the mapping from change type to
version number is where error packages differ from ordinary libraries.

**Ordinary semver** says: breaking API change → major; new feature → minor; bug fix →
patch.

**For error packages**, the API is not only the function signatures. It is:

| Surface | What consumers rely on | Breaks when |
| ------- | --------------------- | ----------- |
| **Types** | The shape of `AppError` | A field is removed, renamed, or its type changes |
| **Codes** | The code strings they compare against | A code is removed or repurposed |
| **Categories** | The status and policy a category implies | A category's status, recovery, or retryability changes |
| **Public messages** | What a user is shown | The wording changes |
| **Public bodies** | The field names in the problem-details body | A field is removed or renamed |
| **Behaviour** | What the adapter does | A mapping, a retry, or a redaction rule changes |

The last one is the trap. **Behavioural changes are invisible in a diff** — a one-line change
to a status map is a `PATCH`-looking diff and a `MAJOR` change in meaning.

### The change classification

| Class | Example | Version | Consumer action |
| ----- | ------- | ------- | ---------------- |
| **Additive** | A new error code in a new domain | **MINOR** | None |
| **Additive** | A new category with a new status | **MINOR** | None (but check nothing switches on "unknown category") |
| **Additive** | A new optional field on `AppError` | **MINOR** | None (JSON consumers must tolerate unknown fields) |
| **Additive** | A new exported function | **MINOR** | None |
| **Behaviour-changing** | A category's status changes (409 → 422) | **MAJOR** | Consumers with golden tests will fail; clients see a new status |
| **Behaviour-changing** | A public message is reworded | **PATCH**\* | None technically; **MAJOR** if the wording is contractual |
| **Behaviour-changing** | The retry policy's attempts change | **MAJOR** | Load characteristics change |
| **Behaviour-changing** | A mapper's classification changes | **MAJOR** | The category consumers switch on may change |
| **Breaking** | A code is removed | **MAJOR** | Consumers matching the code must update |
| **Breaking** | A code is repurposed | **MAJOR** | Worse: consumers matching the code now match a different meaning |
| **Breaking** | A type field is removed or retyped | **MAJOR** | Compile error — good |
| **Breaking** | An exported function's signature changes | **MAJOR** | Compile error — good |
| **Breaking** | A public body field is removed | **MAJOR** | Client contract change |
| **Fix** | A redaction hole is closed | **PATCH** | None |
| **Fix** | A typo in an internal message | **PATCH** | None |

\* The wording rule is a decision, not a law. Acme's rule: **wording is part of the public
contract if a client may display it verbatim.** The public `publicMessage` is contractual;
the internal `message` is not.

### The compatibility promise

The promise the package makes, stated once:

> **Within a MAJOR version, a consumer can upgrade the package without changing its own
> code, and the only behavioural differences will be ones listed in the changelog as
> `MAJOR` — and those are opt-in via the consumer's own registry.**

That last clause is the mechanism that makes a `MAJOR` bump survivable. A behaviour change
that consumers do not want is available as an **override in the consumer's registry**, not
forced on them. The package ships the new default; the consumer that has not opted in keeps
the old behaviour.

### 54.17 — Preventing breaking changes

Breaking changes are prevented by **mechanics**, not by good intentions. Six mechanisms, in
order of how much they prevent:

| # | Mechanism | Prevents | Cost |
| - | --------- | -------- | ---- |
| **1** | **Type-level immutability** — `readonly` fields, `as const` tables, union types for codes | Accidental mutation; typos; unregistered codes | Zero |
| **2** | **Exhaustiveness checks** — `Record<Category, X>` and `satisfies` | A new category without a mapping | Zero |
| **3** | **Registry coverage test** in the consumer's CI | A code the consumer does not have a row for | Low |
| **4** | **Contract snapshot test** in the package | An accidental change to a table | Low |
| **5** | **Additive-first policy** — add, deprecate, remove | Premature removals | Low |
| **6** | **Deprecation window** — remove only after N releases | Breaking removals | Slow |

Mechanism 4 is the one teams skip, and it is the one that catches behavioural changes. A
snapshot test of the generated registry and the category table turns "did we accidentally
change a status?" into a failing test rather than a production surprise.

```ts
// packages/errors/test/contract-snapshot.test.ts
import { expect, it } from "vitest";
import { CATEGORY_POLICY } from "../src/core/category-policy";
import { toMatchSnapshot } from "./snapshot";

it("the category contract has not changed without a major bump", () => {
  expect(toMatchSnapshot(CATEGORY_POLICY)).toMatchSnapshot();
});
```

The snapshot must be updated **deliberately**, and the pull-request template asks "does this
change the contract?" — because the snapshot diff is otherwise invisible in review.

### The deprecation lifecycle

```text
  1. INTRODUCE   the new code, alongside the old. Both registered.
  2. DUAL-EMIT   the service may emit both during a transition.
  3. MIGRATE     consumers move to the new code. Tracked by telemetry.
  4. SUNSET      the old code is marked deprecated in the registry.
                 It is still resolvable; it logs a warning when used.
  5. REMOVE      after the window and after usage reaches zero.
```

The rule that makes step 5 safe: **a code is removed only when its usage telemetry says
zero for a full window.** Not "we announced it" — measured.

```ts
// A deprecated code stays resolvable. Using it logs a warning.
export function registryEntry(code: string): RegistryEntry {
  const entry = REGISTRY[code];
  if (!entry) throw new UnknownErrorCodeError(code);
  if (entry.deprecated) {
    emitWarning({ code, removedIn: entry.deprecated, message: "deprecated error code used" });
  }
  return entry;
}
```

### The version matrix in practice

Acme's package history, with the change class and the consequence:

| Version | Change | Class | Consumer action |
| ------- | ------ | ----- | ---------------- |
| `1.0.0` | Initial core, 15 categories | — | Adopt |
| `1.1.0` | 6 new checkout codes | Additive | None |
| `1.2.0` | `request_id` added to the public body | Additive | None (clients must tolerate unknown fields) |
| `1.2.1` | Redaction hole closed in `context` | Fix | None |
| `1.3.0` | New `ai_token_limit` category | Additive | None |
| `1.4.0` | `rate_limit` retry policy: 2 → 3 attempts | Behaviour-changing | **MAJOR** — but released as `2.0.0` with an opt-in override |
| `2.0.0` | `rate_limit` attempts 2 → 3; `conflict` status 409 → 422 | Behaviour-changing | Opt-in; the old behaviour remains the default for consumers that did not opt in |
| `2.1.0` | New `job_transient` category | Additive | None |
| `2.2.0` | `CHECKOUT_CARD_DECLINED` retired | Breaking (removal) | Only after usage telemetry read zero for 2 minor releases |

Note row 6: the attempt change was a **one-line diff** and still a major bump. That is the
whole point of the classification table — the diff size is irrelevant; the meaning is what
is versioned.

## How it works (mechanics)

The release checklist, run on every package release:

```text
  1. Classify every change: additive | behaviour-changing | breaking | fix.
  2. Additive and fix → MINOR or PATCH.
  3. Behaviour-changing or breaking → MAJOR. Write the migration note.
  4. For a behaviour change, provide the opt-in override in the consumer's registry.
  5. Update the contract snapshot. Read the diff.
  6. Update the changelog with: what changed, who it affects, what to do.
  7. For a removal, check the usage telemetry: zero for a full window.
  8. Publish. Notify the consumers whose code matched a deprecated code.
```

Step 4 is the difference between a `MAJOR` bump that breaks the organisation and one that
does not. A behaviour change with an opt-in override is a `MAJOR` bump that is safe to
adopt at leisure.

## Worked example

The `2.0.0` release, in detail, because it is the release that taught Acme the rules.

The change: the `rate_limit` category's retry policy went from 2 attempts to 3, because
the provider's rate-limit windows had grown. The diff was one line:

```diff
-  rate_limit: { maxAttempts: 2, baseDelayMs: 1_000, maxDelayMs: 5_000, ... },
+  rate_limit: { maxAttempts: 3, baseDelayMs: 1_000, maxDelayMs: 5_000, ... },
```

Classified as **behaviour-changing** (the load characteristic changes), so `2.0.0`.

To keep it safe, the release also shipped:

```ts
// The consumer's registry can keep the old behaviour.
export const billingRegistry = defineRegistry("billing", {
  // ...
}, {
  // Opt-in overrides, per category.
  retryOverrides: {
    rate_limit: { maxAttempts: 2 },
  },
});
```

And the changelog entry:

```markdown
## 2.0.0 — 2026-05-18

### Behaviour changes (opt-in)

- `rate_limit` now retries 3 attempts instead of 2.
  The provider's rate-limit window has grown from 30 s to 90 s; two attempts was no longer
  enough to survive it.

  **Affected:** services that call rate-limited APIs. Under the new policy, a rate-limited
  call occupies a worker for up to 15 s instead of 6 s.

  **Migration:** none required. To keep the previous behaviour, set
  `retryOverrides.rate_limit.maxAttempts = 2` in your registry.
  The override is supported for the whole 2.x line.

### Additive

- New category `ai_token_limit` (422).
- New field `request_id` in the public body.
```

The release reached 11 services. **9** upgraded on the day of the release with no code
change; **2** (the ones with a long-lived worker) added the override in the same week. No
coordinated rollout, no downtime, and the package's own snapshot test caught an
*unrelated* accidental status change in the same release — the `conflict` status was
changed from `409` to `422` by an editor autocomplete — before it was published.

That last point is the payoff: the snapshot test turned a silent breaking change into a
failing test in CI.

## Key data / numbers

- **Surfaces that define the contract: 6** (types, codes, categories, public messages,
  public bodies, behaviour).
- **Version mapping:** additive → **MINOR**; behaviour-changing or breaking → **MAJOR**;
  fix → **PATCH**; wording change → **PATCH** (internal) or **MAJOR** (public message).
- **Compatibility promise:** within a MAJOR version, a consumer can upgrade without code
  changes; behaviour changes are opt-in.
- **Deprecation window: 2 minor releases minimum**, plus a telemetry-zero requirement.
- **Deprecation evidence:** usage telemetry, not announcement. Acme requires **zero usage
  for a full window** before removal.
- **Prevention mechanisms: 6** (type immutability, exhaustiveness, registry coverage test,
  contract snapshot, additive-first policy, deprecation window).
- **Contract snapshot:** the package's own test suite, run on every release; it caught **1**
  accidental `409 → 422` status change in Acme's first year.
- **Adoption of a MAJOR bump:** **9 of 11** services upgraded with no code change; **2**
  needed an override; **0** required a coordinated rollout.
- **Override support:** for the whole `2.x` line — that is, a `MAJOR` bump is reversible
  for consumers for as long as the major line lives.
- **Optional-field rule:** consumers of a JSON body must tolerate unknown fields; this is
  why adding `request_id` was a `MINOR`.

## Real-world use case — Acme SaaS, the patch release that broke production

Early in the package's life, a release went out as `1.2.3` — a `PATCH`. The diff:

```diff
-  conflict: { httpStatus: 409, ... },
+  conflict: { httpStatus: 422, ... },
```

A developer fixed a "wrong status" complaint (a partner had said the `409` was
unhelpful) and shipped it as a patch. The consequences across Acme's 11 services:

- **Every** conflict response became `422`. Clients that retried `409` (correctly, after
  re-reading state) stopped retrying, and **3** of them began showing "validation error" to
  users for what was actually a conflict.
- Two clients' contract tests failed, but **the package was consumed as a versioned
  dependency**, and the services' CI did not run the package's contract snapshot — only the
  package's own CI did, and it passed because the snapshot had been updated in the same
  commit.

The incident lasted **2 hours** before the release was rolled back, and it produced **41**
support tickets.

Three changes came out of it, all of them in the package:

1. **The contract snapshot became a consumer-run check.** The package publishes a
   `contract.json` describing the categories, statuses, and codes. Consumers' CI runs a
   check that fails if a service's observed responses disagree with the contract.
2. **Status changes became a `MAJOR` class in the release checklist**, and the release
   checklist now requires an explicit classification before publishing. There is no
   "patch" that touches a status.
3. **The changelog template changed** to ask "does this change what a consumer receives?"
   and the answer is required in the release checklist.

The lasting rule, now written in the package's `CONTRIBUTING`:

> **A `PATCH` release may not change any status, category, code, public message, or
> behaviour. If it does, it is a `MAJOR` release, no matter how small the diff.**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One version for everything | Simple | Every change is a major | Rarely; a stalled package |
| Strict semver with contract snapshot | Safe; predictable | Slow; every consumer must upgrade eventually | The default |
| Never bump (monorepo, path deps) | No coordination | No isolation; a change is a change everywhere | A monorepo with atomic builds |
| Independent versions per adapter | Flexible | Consumers pin many versions | When adapters genuinely have different lifetimes |
| Behaviour changes without opt-in | Simple | Forced migrations | Only for a pre-1.0 package with no external consumers |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify the change before choosing the version | Pick the version from the diff size |
| Treat status, message, and policy changes as `MAJOR` | Ship a behaviour change as a `PATCH` |
| Ship behaviour changes with an opt-in override | Force a behaviour change on consumers |
| Remove a code only after telemetry shows zero | Remove a code because it was announced |
| Keep the old behaviour overridable for the whole major line | Sunset the old behaviour in the next minor |
| Run the contract snapshot in consumer CI | Assume the package's CI is enough |
| Use a `satisfies`/`Record` type for every table | Let a table lose a key silently |

## Common mistakes

- **The diff-size version.** The most common mistake, and the most expensive one.
- **The silent repurposing.** A code that keeps its name but changes its meaning is the
  worst break, because consumers matching the code keep matching it.
- **The removed export with no replacement.** A `MAJOR` bump is the right call, but ship a
  deprecated alias for one minor release first.
- **The consumer that pins an old version forever.** The package is fine; the consumer is
  accumulating a security and correctness backlog. The deprecation telemetry is what
  surfaces it.
- **The snapshot updated in the same commit as the change.** The snapshot is only a
  safety net if someone reads the diff. A convention that says "read the snapshot diff" is
  part of the release checklist.

## Checklist

- [ ] Every change is classified as additive, behaviour-changing, breaking, or fix.
- [ ] Behaviour changes and removals are `MAJOR`.
- [ ] Behaviour changes ship with an opt-in override.
- [ ] Deprecated codes stay resolvable and warn on use.
- [ ] Removal requires zero usage for a full window.
- [ ] The contract snapshot is in the package's test suite and reviewed in every release.
- [ ] The changelog states what changed, who it affects, and what to do.

## Related

- [The Starter Template and Customization Rules](./02-starter-template-and-customization-rules.md)
- [The Reusable Core Library](../01-concepts/01-the-reusable-core-library.md)
- [Chapter 49 — Error Contract Design and Versioning](../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../../part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)
