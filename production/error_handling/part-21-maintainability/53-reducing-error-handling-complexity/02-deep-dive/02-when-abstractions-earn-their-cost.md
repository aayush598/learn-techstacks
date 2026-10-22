# When Abstractions Earn Their Cost

> Part XXI · Chapter 53 · Sections 53.2, 53.16 · _Estimated reading time: 17 min_
> **Prerequisite:** [Abstraction Cost Analysis](./01-abstraction-cost-analysis.md)

## In one sentence

An abstraction earns its cost when it is **a shared decision with one owner** — and six real
extractions, scored, show that the profitable ones are almost always *tables*, not classes.

## Why this matters in production

Teams rarely lack judgement; they lack **evidence at the moment of the decision**. The
proposal in the design doc sounds right, the duplication is real, and nobody has ever written
down what the shared version will cost. Six weeks later the abstraction exists, it is correct,
and nobody knows how to use it — so the duplication continues *alongside* it.

This file is the evidence: six extractions from real codebases, scored with the
[abstraction cost analysis](./01-abstraction-cost-analysis.md), including the two that were
reverted.

## Core concept

### The six extractions

| # | Subject | Shape chosen | NET | Outcome |
| - | ------- | ------------ | --- | ------- |
| 1 | Postgres unique violation → conflict | Table row in a registry | **−41** | Accepted |
| 2 | Provider `429` → transient + `Retry-After` | Table + a 20-line helper | **−33** | Accepted |
| 3 | HTTP status by category | Table | **−28** | Accepted |
| 4 | Retry attempts by category | Table | **−19** | Accepted |
| 5 | Everything-error-handling | Framework (classes, strategies) | **+167** | Rejected, re-scoped to #3 |
| 6 | Fallback selection by dependency | Strategy interface + 5 implementations | **+6** | Built, then reverted |

Four of six profitable extractions were **tables**. That is the pattern, and it is not a
coincidence: a table is the cheapest way to hold a shared decision, because it has no
vocabulary, no indirection, and no per-call-site configuration.

### Why tables win

| Dimension | Table | Class / strategy | Function with flags |
| -------- | ----- | ---------------- | ------------------- |
| New concepts | 0 | 2–4 | 0–1 |
| Indirection depth | 0–1 | 2–3 | 1 |
| Lines for a 10-case decision | 12 | 180+ | 60 |
| Diff when a case changes | 1 line | 1–3 files | 1–3 files |
| Reviewability | read the table | read the class + all strategies | read the flags |
| Exhaustive check possible | yes (`Record<K, V>`) | no | no |
| Generates documentation | yes | with effort | no |
| Per-call-site configuration | no (keyed by subject) | no | yes (the trap) |

The last row is the important one. A table is **keyed by the subject**, so it cannot drift
into "each caller configures it differently" — the shape itself prevents the most common
decay. A strategy interface permits it, and a flag-per-call-site function *invites* it.

### The reverts, and what they teach

**Extraction #6 — fallback selection by dependency.** A `FallbackProvider` interface with five
implementations, one per dependency (Stripe, Postgres, S3, Redis, the LLM provider). The
analysis scored it **+6** — borderline, and it was accepted because the team expected the
dependency list to grow. It was built, and it was **reverted after 4 months**.

What went wrong: the interface had a method per failure mode (`onTimeout`, `onUnauthorized`,
`onRateLimited`, `onUnavailable`), so adding a new failure mode meant adding a method to the
interface and implementing it in **all five** classes. The abstraction turned every new
failure mode into a **five-file change** — the exact opposite of its purpose.

The replacement was a **map from category to a fallback function**:

```ts
const FALLBACKS: Partial<Record<Category, <T>(ctx: FallbackContext) => T>> = {
  external_api_transient: (ctx) => ctx.cachedValue(),
  external_api_permanent: (ctx) => ctx.emptyValue(),
  ai_provider_transient:  (ctx) => ctx.staleValue(),
};
```

Adding a failure mode is now **one row**. The lesson: **an interface with one method per
failure mode is an interface that will be extended by everyone and maintained by no one.**
Prefer data (a map keyed by category) to polymorphic extension points.

**Extraction #5 — the framework.** Already scored at **+167** in the
[cost analysis](./01-abstraction-cost-analysis.md). The lesson is not "frameworks are bad" —
it is that the *duplication* motivating a framework is usually a *mapping* problem, and a
mapping problem has a mapping-shaped solution.

### The three-question filter, in practice

Before running the full analysis, apply the fast filter. It rejects about **two thirds** of
candidates in under a minute:

```text
  Q1  Does the decision have a natural key?
      (a code, a category, a provider, a dependency)
      NO  →  there is no table-shaped solution; keep it inline.

  Q2  Do all call sites answer the SAME question about that key?
      NO  →  the call sites need different answers; that is not duplication, it is variation.
             Extract the KEY, not the answer.

  Q3  Would a new call site need a new argument, not a new key?
      YES →  you are building a configuration surface. Stop.
```

Q2 is the one that separates real duplication from legitimate variation. Two call sites that
map a timeout differently — an interactive request (fail fast) and a background job (retry for
an hour) — are **not** duplicating a decision. They are making two decisions about the same
subject, and the honest fix is to name both in a table keyed by *context*, not to force them
through one answer.

### 53.2 — Extracting policies, with the three questions applied

The extraction procedure that survives all six cases:

```text
  Step 1  Name the question.          "What does a unique violation mean?"
  Step 2  Find the natural key.       code / category / provider / dependency
  Step 3  Write the answers as data.  a table, one row per key
  Step 4  Write the default.          conservative, explicit, named
  Step 5  Point the call sites at it. one at a time, behaviour preserved
  Step 6  Delete the old code.        if it won't delete, you found a hidden case
  Step 7  Add the exhaustiveness check.  the type system or a lint rule
```

Step 7 is what makes the extraction **durable**. A `Record<Category, Recovery>` forces the
compiler to know every category, so a new category cannot be added without a row. Without
step 7, the table silently develops holes, and the holes are where the drift returns.

### 53.16 — The abstraction-cost ledger

Every accepted extraction gets a ledger row, in the repository, next to the code:

```yaml
- subject: "Postgres unique violation → conflict"
  key: category
  shape: table
  net_score: -41
  call_sites: 4
  re_analyse_when: "call sites exceed 8"
  owner: platform
  added: "2026-03-11"
- subject: "Fallback selection by dependency"
  key: category
  shape: map_of_functions
  net_score: -19          # after the re-scope that replaced the interface
  call_sites: 4
  re_analyse_when: "a new failure mode is added to the interface"
  owner: platform
  added: "2026-05-02"
  replaced: "FallbackProvider interface (2026-03-04 to 2026-05-02)"
```

The `re_analyse_when` field is the part that makes the ledger useful. It converts "we should
revisit this" from a sentiment into a **condition** that can be checked in review or CI.

## How it works (mechanics)

The lifecycle of an accepted abstraction:

```text
  accepted ──▶ adopted ──▶ used ──▶ extended ──▶ (re-analysed) ──▶ replaced
      │           │          │          │                              │
      │           │          │          └─ scope creep: new method/flag  │
      │           │          └─ 3+ call sites?  re-analyse               │
      │           └─ first real divergence: was it worth it?             │
      └─ ledger row written                                           │
```

The **first divergence** is the moment of truth for any extraction. It is the first time the
shared answer had to be different for one caller, and it reveals whether the key was right.
Acme's rule: **the first divergence triggers a re-analysis, not an exception.** The
exception (a special case at one call site) is where the framework starts to rot.

## Worked example

The profitable extraction #1, in full, because it is the common case and it is small.

**Before** — four call sites, four spellings, two status codes:

```ts
// site A (checkout repository)
if (err.code === "23505") throw new ConflictError("duplicate");

// site B (admin API)
if (err.code === "23505") throw new HttpError(409, "Conflict");

// site C (webhook ingest)
if (err.code === "23505") return { status: 422, error: "duplicate" };

// site D (billing worker)
if (err.code === "23505") throw new GenericError("db constraint");
```

**After** — one table, one helper, and an exhaustiveness check:

```ts
// The registry row is the decision.
export const ERROR_REGISTRY = {
  CONFLICT_DUPLICATE_RESOURCE: { category: "conflict", httpStatus: 409, publicMessage: "Resource already exists" },
  // ... every code
} as const satisfies Record<string, { category: Category; httpStatus: number; publicMessage: string }>;

export function statusFor(code: keyof typeof ERROR_REGISTRY): number {
  return ERROR_REGISTRY[code].httpStatus;
}
```

The **key insight** is that the extraction is not a "Postgres translator" at all. It is a
**registry row**. The Postgres-specific code disappeared into the repository layer (which
already owned it), and what remained was the shared decision: "a duplicate is `409`". The
vocabulary cost is **zero new words** — `CONFLICT_DUPLICATE_RESOURCE` already existed as a
domain code.

This is the pattern behind all four profitable extractions: **push the vendor-specific part
down to the layer that owns the vendor, and extract the vendor-agnostic decision upward.**

| Metric | Before | After |
| ------ | ------ | ----- |
| Decision sites | 4 | 1 |
| Lines | 24 | 6 |
| New concepts | 0 | 0 |
| Status codes produced | 409, 409, 422, 500 | 409 |
| Change cost of changing it | 4 files | 1 file |

## Key data / numbers

- **Four of six** profitable extractions were tables; **zero** were classes.
- **Table cost for a 10-case decision: ~12 lines**; equivalent class hierarchy: **180+**
  lines; equivalent flag-based function: **~60** lines.
- **Fast filter rejects ~2 of 3** candidates before the full analysis.
- **Re-analysis triggers:** call sites exceed **2×** the original count; a new **argument**
  appears at a call site; the first **divergence** is requested.
- **The ledger is in the repository**, one row per accepted abstraction, with a
  `re_analyse_when` condition.
- **Observed outcomes:** the interface-based fallback abstraction was **reverted after 4
  months**; the replacement (a map keyed by category) was **1 row per new failure mode**
  instead of one method per class.
- **Reversal cost:** reverting extraction #6 took **1 day** because the abstraction had no
  persisted state — a reminder that error-handling abstractions should stay pure.
- **Review time for PRs touching an extracted table:** **6 min** versus **17 min** for inline
  equivalents.

## Real-world use case — Acme SaaS, the week the abstractions came back

Acme shipped a shared error package, `@acme/errors@1.0.0`, with three modules: a registry, a
mapper, and a `RecoveryAdvisor` class. The first **six weeks** were good: review time on
error-handling PRs fell from **22 min to 7 min**, and four drift incidents were closed.

Then the `RecoveryAdvisor` needed a new capability: "retry the operation but tell the caller
we are degraded while we do". The class needed a `degradeWhileRetrying` option. Adding it
required touching the class, its **builder**, and the **type of the `advice` returned to
callers** — and because the `advice` type was exported, **every consumer's type-check broke**.

Acme had **11 consuming services**. The change took **2 days** to roll out, and the package
had to go to `2.0.0` — a **breaking major bump** for a behaviour that a table row would have
expressed in one line.

The post-mortem action was to re-run the cost analysis on every exported member of the
package. The `RecoveryAdvisor` scored **+11**; the registry and mapper scored **−54** and
**−29**. The advisor was removed in `3.0.0` and replaced with a `RECOVERY` table plus a
`recoveryFor(category, context)` function. The lesson was recorded in the package's ADR:

> **An exported abstraction is a permanent promise.** Re-analyse every exported member
> before changing it, and prefer data (tables) to classes, because data changes are additive
> and class changes are not.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Table keyed by subject | Cheapest; exhaustive; diffable | Needs a natural key | The default for any repeated decision |
| Function with flags | Flexible | Configuration surface; drift | ≤ 2 call sites with genuinely different needs |
| Strategy interface | Extensible per type | Every new case is an N-file change | Rarely; only when the set of *implementations* varies, not the set of cases |
| Base class hierarchy | Familiar OOP | Deep hierarchies; shared mutable state | Legacy code only |
| No extraction | Simple | Drift | < 3 copies |
| Full framework | Uniformity | Highest cost; permanent export promise | Many teams, many repos, and a dedicated owner |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Extract the vendor-agnostic decision | Extract a vendor-specific translator |
| Key tables by the subject | Key them by the layer |
| Re-analyse at the first divergence | Add an exception at the first divergence |
| Keep a cost ledger in the repository | Extract and forget |
| Prefer a table to a class for decisions | Export a class that consumers will depend on |
| Re-analyse exported package members | Change an exported abstraction as a "small fix" |

## Common mistakes

- **Extracting the mechanism instead of the decision.** A `PostgresErrorTranslator` shared
  across services; the shared decision was never "how Postgres errors work".
- **An interface with one method per failure mode.** Every new mode becomes an N-file change.
- **Special-casing at the first divergence.** The exception is the seed of the next framework.
- **Exporting everything.** An exported member is a promise; only export what consumers
  genuinely need.
- **Never measuring the revert.** Extraction #6 was reverted without recording that a map
  would have been cheaper — so the next team would repeat it.

## Checklist

- [ ] The subject has a natural key and a single question.
- [ ] The three-question fast filter passes.
- [ ] The cost analysis has been run and the net score is ≤ 0.
- [ ] The shape is a table unless there is a specific reason otherwise.
- [ ] The exhaustiveness check exists (type-level or lint-level).
- [ ] A ledger row records the score and the re-analysis trigger.
- [ ] Every exported member has been re-analysed before a change to it.

## Related

- [Abstraction Cost Analysis](./01-abstraction-cost-analysis.md)
- [Extracting Policies Without Over-Abstraction](../01-concepts/02-extracting-policies-without-over-abstraction.md)
- [Finding and Measuring Repetition](../01-concepts/01-finding-and-measuring-repetition.md)
- [Chapter 54 — Reusable Error-Handling Infrastructure](../../54-reusable-error-handling-infrastructure/README.md)
