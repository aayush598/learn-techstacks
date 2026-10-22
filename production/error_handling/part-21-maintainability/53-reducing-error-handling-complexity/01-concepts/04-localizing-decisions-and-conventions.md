# Localizing Decisions and Conventions

> Part XXI · Chapter 53 · Sections 53.9, 53.10, 53.11, 53.12 · _Estimated reading time: 17 min_
> **Prerequisite:** [Simplifying Conditionals, Translation, and Retries](./03-simplifying-conditionals-translation-and-retries.md)

## In one sentence

A decision is **locally discoverable** when a developer can answer "where is this decided?"
in one search — and the practical test of an error-handling standard is not whether it is
written down, but **how many files must change** when the system grows.

## Why this matters in production

Every error-handling convention eventually faces the same three events:

1. A new error code appears.
2. A new provider (or a new provider failure) appears.
3. A new service or package appears.

At each event, the team's response reveals whether the conventions were real. If adding a
code takes **six edits in four directories**, the convention is documentation, not structure —
and the shortcut is to skip the registry, hardcode a status, and move on. The system degrades
silently, one PR at a time.

## Core concept

### 53.9 — Easy-to-locate decisions

"Easy to locate" has a precise meaning: **one search returns the answer**, and the answer is a
table row rather than a code fragment.

| Decision | Where it lives | Search that finds it |
| -------- | --------------- | --------------------- |
| What code means | the registry for that domain | `rg "CHECKOUT_CARD_DECLINED"` |
| What the client sees | the HTTP mapping table | `rg "CATEGORY_HTTP"` |
| What is retryable | the retry policy table | `rg "RETRY_POLICIES"` |
| What the recovery is | the recovery policy table | `rg "RECOVERY"` |
| Where a boundary is | the boundary map in the architecture doc | `rg "boundary"` in `docs/` |
| Who owns a code | the registry row's `owner` field | `rg "owner: payments"` |

Three properties make a decision locatable:

- **Named.** The table has a name that describes the question, not the mechanism
  (`CATEGORY_HTTP`, not `httpMap`).
- **Total.** The question has an answer for every subject, so a search for the *subject*
  always finds an answer, not a gap.
- **Co-located with its siblings.** All answers to one question live in one file. If
  "what does a decline mean" is answered in the registry, the HTTP table, and the job table,
  it is not locatable.

The **co-location** rule is the one teams break most. A mapping split across "one table per
layer" is one decision in three places. Split by **subject** (code, category, provider), not
by layer.

### 53.10 — Predictable conventions

A convention is predictable when a developer can **predict the outcome before looking**. The
three most predictable conventions in error handling:

| Convention | Prediction a developer can make |
| ---------- | -------------------------------- |
| "Every code is registered" | "If I emit a code, the registry has a row, and the registry decides the status" |
| "Layers never translate except at boundaries" | "If I am inside a layer, the error I see is already ours" |
| "The registry is the only source of HTTP status" | "No `res.status(...)` in a feature file" |

The third one is the most valuable and the least enforced. A `res.status(422)` inside a
feature handler is a **decision site** that has escaped the table, and it will eventually
disagree with the table.

```ts
// ❌ A decision that escaped the table.
if (validationFailed) res.status(422).json({ error: "invalid" });

// ✅ The table decides; the handler asks.
res.status(statusFor("VALIDATION_FAILED")).json(problemFor(err));
```

Predictable conventions also include **naming**: a code is `DOMAIN_CONDITION`, uppercase,
underscored, stable, and never derived from a class name or a message. A developer who sees
`CHECKOUT_CARD_DECLINED` knows what it is before opening the file.

### 53.11 — Minimizing changes for a new error

The **change cost** of adding a new error is the single most useful maintainability metric in
this book. Write it down as a number and track it.

```text
CHANGE COST OF ADDING A NEW ERROR CODE

  1. Define the code + category + message          → 1 file (domain registry)
  2. Add the registry row                           → 1 file (same file, ideally)
  3. Add the HTTP mapping                           → 0 files (inherited from the category)
  4. Add the retry/recovery mapping                 → 0 files (inherited from the category)
  5. Add a test                                     → 1 file

  TOTAL: 2 files, ~12 LOC
```

**The inheritance is the trick.** Steps 3 and 4 are zero because the HTTP status, the retry
policy, and the recovery policy are keyed by **category**, and a new code inherits from its
category. When a code needs its own HTTP status, that is a signal worth investigating: it
usually means the code is in the wrong category, or the category is too coarse.

The contrast with the bad version:

```text
CHANGE COST OF ADDING A NEW ERROR CODE (before)

  1. Define the class                          → 1 file
  2. Throw it from the service                  → 1 file (feature)
  3. Map it to 422 in the HTTP handler          → 1 file
  4. Map it in the job runner                   → 1 file
  5. Map it in the webhook handler              → 1 file
  6. Add it to the docs                         → 1 file
  7. Add tests for each mapping                 → 3 files

  TOTAL: 8 files, ~70 LOC, and 3 chances to diverge
```

**Target: ≤ 3 files** (definition, registry row, test) for a routine new code. Every extra
file is a chance for the code to behave differently in two places.

### 53.12 — Minimizing changes for a new provider

A new provider is the bigger event, because it can touch translation, retry, timeout, and
fallback. The convention that keeps this cheap is **provider isolation**: everything a provider
can do lives behind one adapter.

```text
  ┌─────────────────────────────────────────────────────────┐
  │ Feature code (Checkout) — knows nothing about Stripe   │
  └───────────────────────────┬─────────────────────────────┘
                              │ uses our categories only
  ┌───────────────────────────▼─────────────────────────────┐
  │ Provider adapter (stripe.ts)                            │
  │   • normalise vendor errors  → our categories            │
  │   • own the timeout                                      │
  │   • own the retry policy                                 │
  │   • own the fallback                                     │
  └─────────────────────────────────────────────────────────┘
```

The **change cost of a new provider** should be: **1 new adapter file + 1 registry row per
provider error + 1 test**. If adding a provider requires editing the HTTP layer or the job
runner, the provider is leaking upward, and the leak will be paid again on the next provider.

| Provider | Files touched to add it | Target |
| -------- | ------------------------ | ------ |
| Stripe (first provider) | 12 | — |
| Slack (after the adapter convention) | **3** | 3 |
| OpenAI (after the adapter convention) | **4** | ≤ 5 |

The two extra files for a provider are usually: a provider-specific code registry (when the
provider's errors are worth naming publicly) and a provider-specific test.

### The convention summary

```text
CONVENTIONS THAT MAKE GROWTH CHEAP

  • One registry per domain; one row per code; the row carries the category.
  • Status, retry, and recovery are keyed by CATEGORY, not by code.
  • Every provider lives behind one adapter that owns timeout, retry, and fallback.
  • No HTTP status literal outside the mapping table.
  • Adding a code touches ≤ 3 files. Adding a provider touches ≤ 5.
```

## How it works (mechanics)

To find where a decision is *supposed* to live, ask three questions in order:

```text
  Q1  What is the SUBJECT of the decision?      → code, category, provider, operation
  Q2  What is the QUESTION?                     → status? retry? recovery? context?
  Q3  Where does a reader EXPECT the answer?    → the table named after the question
```

Q3 is the one that is usually wrong. Developers expect "what does this category return to
the client?" in a file called something like `http-mapping.ts`, and they expect it to be the
*only* place a status appears. When the answer is somewhere else, you have a discoverability
bug — and the fix is to move the answer, not to document the new location.

## Worked example

Acme added an OpenAI-backed "summarize" feature to `AgentRun`. The question was: *what does it
take to add this provider?* The team measured it before writing the adapter, and the answer
was **11 files**.

| File | Why it was needed |
| ---- | ----------------- |
| `providers/openai.ts` | The adapter (expected) |
| `providers/openai-errors.ts` | Normalisation table (expected) |
| `http/ai-mappings.ts` | New provider statuses (not expected) |
| `http/handler.ts` | Special-case branch for AI errors (not expected) |
| `jobs/agent-run.ts` | Retry for AI timeouts (not expected) |
| `docs/error-codes.md` | New code table (expected) |
| 4 more | Timeout constants, feature flags, test fixtures, a wrapper |

The team then applied the convention: **move the AI-specific answers into the adapter and
key the rest by category**. The result:

```ts
// Before: AI errors had their own status table and their own branch in the handler.
// After: AI errors are categories like every other error.

const CATEGORY_HTTP: Record<Category, { status: number; code: string }> = {
  // ...
  ai_token_limit:        { status: 422, code: "AI_TOKEN_LIMIT" },
  ai_provider_transient: { status: 503, code: "AI_PROVIDER_UNAVAILABLE" },
  ai_provider_permanent: { status: 502, code: "AI_PROVIDER_REJECTED" },
};
```

The next provider — a second model vendor — took **4 files**: the adapter, the normalisation
table, the registry rows, and the test. The change cost of a provider had fallen from **11 to
4**.

## Key data / numbers

- **Change cost target, new error code:** ≤ **3 files**, ≤ **15 LOC** of non-test code.
- **Change cost target, new provider:** ≤ **5 files** (adapter, normalisation, registry rows,
  test, and at most one extra).
- **Measured before/after at Acme:** new provider **11 files → 4 files**; new error code
  **8 files → 2 files**.
- **Registry coverage:** **100%** of codes have a row; CI fails otherwise.
- **Status literals outside the mapping table:** target **0**; lint rule enforceable.
- **Decision-site budget:** ≤ **1** decision site per (question, subject) pair. Two sites for
  one question is a defect, not a choice.
- **Naming convention:** `<DOMAIN>_<CONDITION>`, uppercase, `snake_case`, e.g.
  `CHECKOUT_CARD_DECLINED`. Never derived from a class name, file name, or message text.
- **Review time impact:** error-handling review of a new-code PR fell from **19 min** to
  **5 min** after the conventions were applied to Acme's `Checkout` service.
- **Documentation sync:** a code without a registry row fails CI in **< 5 s**.

## Real-world use case — Acme SaaS, the provider that broke the build

Acme's third integration provider was a scheduling service. Adding it took **two sprints**,
not because the integration was hard but because the error handling had no home:

- The provider's `409` was mapped to `500` in the scheduler adapter.
- The API layer had a special case for the provider's rate-limit response.
- The nightly reconciliation job had **its own** retry policy, with **20 attempts**.
- The provider's error codes appeared in the API documentation with **no** registry entry, so
  the docs and the code had already diverged.

The last one was the most expensive: the public API documentation promised a `429` with a
`RATE_LIMITED` body, and the API returned `500` with `{"error":"internal"}`. **3 of 4,800
daily API calls** hit the rate limit during a customer batch import, and all 3 produced
internal errors that paged the on-call engineer.

The fix was the convention, applied mechanically: the provider got an adapter, its failures
became categories, its retry policy moved into the shared table, and its codes entered the
registry. The reconciliation job's twenty attempts became **five with exponential backoff**,
which alone removed an estimated **2.1 million** redundant API calls per quarter during
incidents.

The structural lesson: **the cost of an integration is set by the day you add it, not by the
code you write.** If there is no adapter convention, every provider multiplies your
decision sites.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One central table for everything | Total, one place | Grows past reading; cross-layer coupling | Small systems, ≤ 30 codes |
| Table per domain, shared category tables | Scales; domains stay independent | Requires the category taxonomy to be stable | Medium and large systems |
| Table per layer (status here, retry there) | Each layer owns its concern | One decision split across layers | Never, for the same question |
| Convention documented, no structure | Cheap to write | Not followed under pressure | As a supplement, never instead |
| Structure only, no documentation | Always accurate | Opaque to newcomers | Alongside documentation, never instead |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key status, retry, and recovery by category | Maintain a per-code status table |
| Put every provider behind one adapter | Let features call providers directly |
| Measure the change cost of a new code | Accept "it is only three files" without counting |
| Name the tables after the question | Scatter one question across several files |
| Keep the registry total | Emit a code that the registry does not know |
| Enforce the conventions in CI | Rely on review to catch a stray `res.status(422)` |

## Common mistakes

- **A per-code status table.** Fifty codes means fifty rows to maintain, and a new code
  needs a row in three tables instead of one.
- **The provider leak.** A feature imports the provider SDK and maps its errors inline. The
  first provider change now touches the feature.
- **The special case.** One provider's `429` gets a branch in the generic handler "just this
  once". It is never just once.
- **Splitting a question by layer.** "What does a decline mean" answered in the repository and
  again in the HTTP layer.
- **Convention without a gate.** A rule no CI job checks is a rule that is broken within one
  sprint.

## Checklist

- [ ] You can state the change cost of adding an error code, in files, and it is ≤ 3.
- [ ] You can state the change cost of adding a provider, in files, and it is ≤ 5.
- [ ] Every question about a failure has exactly one decision site, named after the question.
- [ ] Status, retry, and recovery are keyed by category, not by code.
- [ ] No provider is called from feature code.
- [ ] A CI check fails when a code is missing from the registry.

## Related

- [Extracting Policies Without Over-Abstraction](./02-extracting-policies-without-over-abstraction.md)
- [Readable Business Logic and the Easy Path](./05-readable-business-logic-and-the-easy-path.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)
