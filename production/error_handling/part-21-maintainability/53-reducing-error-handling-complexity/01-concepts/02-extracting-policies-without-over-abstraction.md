# Extracting Policies Without Over-Abstraction

> Part XXI · Chapter 53 · Sections 53.2, 53.3, 53.16 · _Estimated reading time: 18 min_
> **Prerequisite:** [Finding and Measuring Repetition](./01-finding-and-measuring-repetition.md)

## In one sentence

A **policy** is a named, table-driven answer to "what should happen for this kind of failure" —
and extracting one is worth it only when the extraction removes more complexity than it adds.

## Why this matters in production

Teams that need consistency reach for the same lever: a shared helper, a base class, a config
file. Some of those work. Most of them fail in one of two ways:

- **The abstraction is too thin.** It wraps one function and adds a parameter for every
  variation, so call sites pass four arguments to express what a local `if` said in one line.
- **The abstraction is too broad.** It becomes a framework with its own concepts, its own
  vocabulary, and its own bugs. When the framework is wrong, every consumer is wrong at once.

The failure is always the same shape: **the abstraction's own complexity exceeds the
duplication it replaced.** The discipline is to compare those two numbers explicitly, which is
what the [abstraction cost analysis](../02-deep-dive/01-abstraction-cost-analysis.md) does.

## Core concept

### 53.2 — What a policy is

A policy answers a question that the code would otherwise answer by branching. The questions
that produce policies in error handling:

| Question | Policy name | Output |
| -------- | ----------- | ------ |
| What category is this? | classification policy | category |
| What does the client see? | external-mapping policy | status, code, public message |
| Is it safe to retry? | retry policy | attempts, delay, deadline |
| What is the recovery? | recovery policy | fail / degrade / compensate / terminate |
| What is attached? | enrichment policy | context fields, redaction rules |

A policy has a **name**, a **shape**, and a **default**. Those three things are what make it
extractable: a named thing with a default can be overridden at one place, and the default is
the current behaviour, so extraction is safe.

```ts
// A policy is data, not a chain of ifs.
export interface RetryPolicy {
  readonly maxAttempts: number;       // total attempts, including the first
  readonly baseDelayMs: number;
  readonly maxDelayMs: number;
  readonly jitter: boolean;
  readonly totalDeadlineMs: number;
  readonly retryOn: readonly Category[];
}

export const DEFAULT_RETRY: RetryPolicy = {
  maxAttempts: 3,
  baseDelayMs: 200,
  maxDelayMs: 2_000,
  jitter: true,
  totalDeadlineMs: 8_000,
  retryOn: ["external_api_transient", "database_transient", "dependency_unavailable"],
};
```

The moment you can name it, you can talk about it, test it, override it, and point at it in a
review. That is the real value of extraction — not fewer lines.

### The three shapes of an extracted policy

| Shape | Looks like | Use when |
| ----- | ---------- | -------- |
| **Table** | `Record<code, entry>` | The answer depends on the *subject* (a code, a category, a provider) |
| **Predicate chain** | An ordered list of `if`s with a default | The answer depends on *precedence* (first match wins) |
| **Strategy** | A function passed in | The answer depends on *runtime state* (tenancy, feature flag) |

Tables are the default choice. They are diffable, exhaustively checkable, and generate
documentation. A predicate chain is a table with a hidden ordering. A strategy is a table with
a runtime parameter — useful, but never the first move.

### 53.3 — Avoiding unnecessary abstractions

Four tests catch an abstraction that is not earning its keep:

**Test 1 — Call-site test.** Does the abstraction have at least **three** call sites that
genuinely share the decision? Two call sites usually mean the abstraction needs a flag, and a
flag-per-call-site abstraction is a shared function with extra steps.

**Test 2 — Configuration test.** Can you express every call site with the *same* arguments? If
each call site passes a different value for most parameters, the abstraction is a parameter
bag; inline it.

**Test 3 — Vocabulary test.** Does the abstraction introduce a word that the domain does not
already use? If you need to explain "retry scope" or "error policy tier" before using it, the
concept tax is real.

**Test 4 — Removal test.** If you deleted the abstraction and pasted the body at each call
site, would any call site become *harder to read*? If not, the abstraction is ceremony.

```ts
// ❌ Parameter-bag abstraction: every call site passes different values.
class Policy {
  constructor(
    private readonly category: Category,
    private readonly maxAttempts: number,
    private readonly delayMs: number,
    private readonly jitter: boolean,
    private readonly deadlineMs: number,
    private readonly onExhausted: "fail" | "queue" | "page",
  ) {}
}

// ✅ Table: the subject is the key, the answer is the value.
const RETRY: Partial<Record<Category, RetryPolicy>> = {
  external_api_transient: { maxAttempts: 3, baseDelayMs: 200, maxDelayMs: 2_000, jitter: true, totalDeadlineMs: 8_000 },
  database_transient:     { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1_000, jitter: true, totalDeadlineMs: 5_000 },
};
```

### 53.16 — Abstractions that cost more than they save

The clearest way to see this is to count the **decision sites** an abstraction creates. A
helper that hides one decision but requires the caller to make three new ones has moved the
complexity, not removed it.

| Symptom | What it really means | Fix |
| ------- | -------------------- | --- |
| The helper takes 5+ parameters | It is a parameter bag | Inline it, or make it a table |
| The helper has a boolean flag per variation | It is a strategy in disguise | Split into two named things |
| The helper's name needs a paragraph | Vocabulary tax | Rename, or split it |
| Only one caller uses the "flexible" path | YAGNI on the flexible path | Delete the flexible path |
| Callers import 3 modules to use it | Coupling tax | Reduce the surface |
| Nobody can say what the default is | No safe default | Give it one, or don't extract it |
| It has its own tests but no users | Speculative generality | Delete it |

> ⚠️ **Hazard.** The most expensive abstraction is not the wrong one — it is the one that is
> *believed* to be right. A shared framework gets defended in review long after its users have
> stopped needing it, because removing it feels like removing a standard.

### The extraction rule of thumb

```text
  extract a policy when:
    ✓ same decision, ≥ 3 call sites
    ✓ the same arguments work everywhere
    ✓ it has a safe default that preserves today's behaviour
    ✓ it introduces no new vocabulary
    ✓ extraction saves ≥ 80 LOC or removes a drift risk you have actually observed
```

If two of those fail, **do not extract yet**. Write the duplication down, and revisit after the
fourth copy shows up.

## How it works (mechanics)

Extraction is a **behaviour-preserving refactor** in four steps. The order matters: each step
leaves the system working, so the refactor can be stopped at any point.

```text
  Step 1  Write the decision down as a table, in the module that owns it.
  Step 2  Point the first call site at the table. Behaviour must not change.
  Step 3  Move the remaining call sites, one at a time, deleting as you go.
  Step 4  Delete the old code. If it does not delete cleanly, you missed a case.
```

Step 4 is the real test. If the old block does not delete cleanly, there was a hidden
behaviour — a special case that was never written down. That is a **finding**, and it usually
explains the drift you were chasing.

## Worked example

Acme's `ExportJob` had the retry decision in four places: the job runner, the S3 adapter, the
database writer, and the queue consumer wrapper. Each had its own numbers.

```ts
// ── Before: the same decision, four times, three different answers ──
const EXPORT = {
  maxAttempts: 3, delayMs: 1_000, backoff: 2, jitter: false, deadlineMs: 30_000,
};
// job runner:   maxAttempts 3, delay 1000, no jitter
// s3 adapter:   maxAttempts 5, delay 500,  jitter
// db writer:    maxAttempts 3, delay 2000, no jitter
// consumer:     maxAttempts 10, delay 0,    no jitter
```

The consumer's ten attempts with no delay was the dangerous one: during an S3 outage, **10,000
concurrent export jobs** hammered S3 every second, and the outage lasted **47 minutes**.

Extraction produced a table keyed by category, with a default for everything not listed:

```ts
export const RETRY_POLICIES: Partial<Record<Category, RetryPolicy>> = {
  external_api_transient: { maxAttempts: 3, baseDelayMs: 500, maxDelayMs: 8_000, jitter: true, totalDeadlineMs: 30_000 },
  database_transient:     { maxAttempts: 3, baseDelayMs: 200, maxDelayMs: 4_000, jitter: true, totalDeadlineMs: 15_000 },
  job_transient:         { maxAttempts: 5, baseDelayMs: 5_000, maxDelayMs: 300_000, jitter: true, totalDeadlineMs: 900_000 },
};

export function retryPolicyFor(category: Category): RetryPolicy {
  return RETRY_POLICIES[category] ?? NO_RETRY;   // the safe default
}
```

The `job_transient` row is where the job's delay lives: five attempts, five-second base, a
**5-minute cap** on a single delay, and a **15-minute total deadline**. That single row
replaced four divergent behaviours and is now the only place a retry number appears.

## Key data / numbers

- **Extraction trigger:** ≥ **3** call sites sharing a decision.
- **Break-even:** ≥ **80 LOC** saved, or one observed drift incident of equal or greater cost.
- **Policy shape preference:** table → predicate chain → strategy, in that order.
- **Parameter count ceiling:** **5** named parameters in a policy object; beyond that, use a
  table.
- **Default rule:** a policy table is **total** — every category resolves, and unresolved
  categories get the conservative default (`NO_RETRY`), never "unbounded".
- **Acme's `ExportJob` result:** 4 decision sites → **1**; retry attempts bounded at **5**;
  maximum single delay **300 s**; S3-outage amplification reduced from **10×** to **3×**.
- **Cost of the framework path (rejected):** a proposed 4,000-line shared framework would have
  added **1** concept, **9** configuration points, and **0** new behaviours. It was rejected
  under the removal test.

## Real-world use case — Acme SaaS's `AgentRun`

`AgentRun` calls an LLM provider, and the provider's failure vocabulary changed **four times in
one year** (new rate-limit header, a new `503` on overload, a model deprecation, a token-limit
error with a new body shape). Each change meant editing the provider adapter, the service
layer, the job runner, and the API handler — **four files, four services, in the same week**.

The team tried two responses. The first was a shared "provider error normaliser" class with
eleven subclasses and a `map()` method per provider. It took **three weeks** to build, was
understood by two people, and broke when the provider added a rate-limit header because the
`map()` chain had a `default` that swallowed the new case.

The second response was a **table with a default and a lint rule**:

```ts
// The whole mapping. It grows by one row when the provider grows a new failure.
const PROVIDER_FAILURES: Record<string, Category> = {
  rate_limit_exceeded: "external_api_transient",
  overloaded:          "external_api_transient",
  invalid_api_key:     "external_api_permanent",
  context_length_exceeded: "ai_token_limit",
};
```

A provider change became a **one-line diff** plus one test. The abstraction cost analysis
scored it: 3 call sites, 38 LOC saved, one new word (`Category`, already in the domain). The
first attempt failed the vocabulary test and the removal test; the second passed both.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No abstraction | Zero indirection | Duplication, drift | < 3 copies, or contexts that must diverge |
| Shared table | Diffable, total, documented | Needs a subject to key on | Same subject, different decisions — the default choice |
| Predicate chain | Handles precedence | Hidden ordering, harder to review | Precedence genuinely matters |
| Strategy function | Handles runtime state | Harder to enumerate, harder to document | Behaviour varies per tenant or flag |
| Framework | Uniformity at scale | Highest cost, slowest adoption | Many teams, many repos, a stable domain, and a budget |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every policy a conservative default | Leave a category unresolved "for now" |
| Extract the decision, not the syntax | Extract a function that just wraps one line |
| Keep policy tables total | Add a `default` branch that guesses a category |
| Delete the old code after extraction | Keep the old path "as a fallback" |
| Re-measure after extracting | Assume the duplication stays gone |

## Common mistakes

- **Extracting at the wrong level.** The shared thing was a *string format*, not a *decision* —
  so the extraction saved nothing and added a helper.
- **A policy with no default.** The table is partial, so an unlisted category throws at the
  worst possible moment.
- **Sharing across bounded contexts.** Two services that must evolve independently share a
  table, and neither can ship without the other.
- **The framework as a substitute for a decision.** A framework that does not decide anything
  is just indirection with a README.
- **Never deleting the original.** Two implementations survive, and the drift returns with a
  new name.

## Checklist

- [ ] Every extracted policy has a name, a shape, and a conservative default.
- [ ] The old implementation is deleted, not kept as a fallback.
- [ ] The abstraction passes the four tests: call sites, configuration, vocabulary, removal.
- [ ] The decision table is total, and the default is conservative.
- [ ] The extraction is recorded in the duplication report with the new copy count (**1**).

## Related

- [Finding and Measuring Repetition](./01-finding-and-measuring-repetition.md)
- [Abstraction Cost Analysis](../02-deep-dive/01-abstraction-cost-analysis.md)
- [When Abstractions Earn Their Cost](../02-deep-dive/02-when-abstractions-earn-their-cost.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
