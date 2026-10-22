# A Complexity Budget for a Feature

> Part XXI · Chapter 53 · Sections 53.9, 53.13, 53.15 · _Estimated reading time: 19 min_
> **Prerequisite:** [Readable Business Logic and the Easy Path](../01-concepts/05-readable-business-logic-and-the-easy-path.md)

## In one sentence

A **complexity budget** is a per-feature limit on error-handling surface — files, lines,
decision sites, and failure branches — that is checked automatically, so the cost of an
error-handling system is a number rather than a vibe.

## Why this matters in production

Complexity budgets work like performance budgets: you do not need them to be exact, and you do
not need them to be zero. You need them to be **visible before the debt is invisible**.

Without a budget, a feature's error-handling surface grows by accretion, and the growth is
invisible in review because each individual change is small:

- A new failure adds a branch in the service: **+6 lines**.
- The branch needs a status: **+2 lines** in the handler.
- The job needs its own version: **+8 lines**.
- A test for each: **+20 lines**.

Four PRs, 36 lines, and the feature now has **four** decision sites for one question. No
single PR looked wrong. The budget is what makes the pattern visible: the fourth PR is the
one that crosses the limit, and the check fires *there*, when it is still cheap to fix.

## Core concept

### The four dimensions of the budget

| Dimension | What it limits | Why it is a good proxy |
| --------- | -------------- | ---------------------- |
| **Files** | Number of files a feature's error handling spans | More files = more places to look = longer onboarding |
| **Lines** | Total error-handling lines in the feature | A proxy for the amount of branching to read |
| **Decision sites** | Places that answer a failure question | The direct measure of duplication risk |
| **Failure branches** | Branches inside business logic | The measure of how much the domain rule is buried |

The important one is **decision sites**. Lines can be reduced without reducing decisions
(compressing code); decisions cannot be reduced without changing structure. Budget the
decision sites, and use the others as sanity checks.

### The budget for a feature

```yaml
# complexity-budget.yml — one entry per feature
features:
  checkout:
    max_error_files: 3          # errors.ts, adapters.ts, tests
    max_error_lines: 120        # non-test error-handling lines
    max_decision_sites: 6       # places that answer a failure question
    max_failure_branch_ratio: 0.20   # failure branches / total lines in the feature
  export:
    max_error_files: 3
    max_error_lines: 150        # this feature legitimately has more outcomes
    max_decision_sites: 8
    max_failure_branch_ratio: 0.25
```

The budgets are **per feature**, not global, and they are set from the *shape of the feature*:

| Feature shape | Decision sites | Why |
| ------------- | -------------- | --- |
| Simple CRUD | 3–4 | One validation family, one not-found, one conflict |
| Payment / checkout | 6–8 | External provider, ambiguous outcomes, compensation |
| Background export | 6–8 | Provider, storage, partial progress, checkpointing |
| Webhook ingest | 5–7 | Signature, duplicates, provider, ordering, replay |
| LLM agent | 8–10 | Provider, token limits, tool failures, per-step partial state |

Setting the budget from the feature shape is what makes it fair. A budget that is too tight
gets waived; a budget that is too loose is not a budget.

### How the check works

The check is a script, not a review convention. It has to run in **under 10 seconds**, or
nobody runs it.

```ts
// scripts/check-error-budget.ts — pseudo-implementation
import { readdirSync, readFileSync } from "node:fs";

interface Budget {
  max_error_files: number;
  max_error_lines: number;
  max_decision_sites: number;
  max_failure_branch_ratio: number;
}

function countDecisionSites(dir: string): number {
  // A decision site = a call to a mapping/registry lookup, or a branch on an error field.
  const pattern = /(statusFor|statusFor\(|categoryOf\(|problemFor\(|retryPolicyFor\(|recoveryFor\(|if\s*\(\s*(err|error)\b)/g;
  let total = 0;
  for (const file of walk(dir)) {
    if (!file.endsWith(".ts") || file.includes(".test.")) continue;
    total += (readFileSync(file, "utf8").match(pattern) ?? []).length;
  }
  return total;
}
```

The exact pattern matters less than the property it guarantees: **the check counts something
objective**, and the objective is defined once, in one file, so two people do not argue about
what "a decision site" means.

> ⚠️ **Hazard.** A budget check that can be silenced with a per-file `// budget: ignore`
> comment becomes a comment convention within a quarter. If you need an escape hatch, make it
> a **dated, expiring exception** in the budget file, owned and reviewed — not a comment in
> the code.

### What a budget does *not* do

- It does not say "write less code". It says "keep the number of *decisions* bounded".
- It does not forbid an error-handling file. Acme's `export` feature has three, and that is
  fine.
- It does not measure quality. A feature can meet its budget and still be wrong — that is
  what Chapter 51's correctness properties are for.
- It does not apply to shared platform modules. Their budget is the *abstraction cost
  analysis* from Chapter 53, not a line count.

## How it works (mechanics)

The budget review, once per quarter, is a **read-and-adjust** exercise:

```text
  1. Run the check. Record every feature over budget.
  2. For each over-budget feature, decide:
       - is the budget wrong?            → adjust the budget, with a note
       - is the feature wrong?           → refactor (Chapter 53 concepts)
       - is the feature legitimately big? → raise the budget, with a note
  3. Never lower a budget to make a check pass. Lower it only after a refactor.
  4. Record the decision in the budget file, with a date and a reason.
```

Step 3 is the rule that keeps the budget meaningful. A budget that ratchets downward is a
quality gate; a budget that ratchets upward is a form.

## Worked example

The `ExportJob` feature at Acme, before and after the budget existed.

**Before** (the numbers from the actual repository):

```text
export/
  errors.ts                  84 lines
  errors/adapter.ts          61 lines
  errors/mapping.ts          47 lines
  errors/retry.ts            39 lines
  export-runner.ts          210 lines   (78 of them error branches)
  export-sink.ts             66 lines   (24 of them error branches)
  export-checkpoint.ts       41 lines   (12 of them error branches)
  ─────────────────────────────────────────────
  error files:  4          (budget: 3)          ❌ over
  error lines:  231        (budget: 150)        ❌ over
  decision sites: 14        (budget: 8)          ❌ over
  failure branch ratio: 114/317 = 0.36           ❌ over (budget 0.25)
```

**After** the refactor described in
[Readable Business Logic and the Easy Path](../01-concepts/05-readable-business-logic-and-the-easy-path.md):

```text
export/
  errors.ts                  62 lines   (codes + outcomes + mapping)
  errors/adapter.ts          38 lines   (sink + checkpoint normalisation)
  export-runner.ts            96 lines   (24 error lines)
  export-sink.ts              48 lines   (6 error lines)
  ─────────────────────────────────────────────
  error files:  2          (budget: 3)          ✅
  error lines:  106        (budget: 150)        ✅
  decision sites: 7         (budget: 8)          ✅
  failure branch ratio: 30/182 = 0.16            ✅
```

Note what disappeared: `errors/mapping.ts` and `errors/retry.ts` were **deleted**, not merged.
The mapping moved into the shared `CATEGORY_HTTP` table in the platform layer (one decision
site for the whole service), and the retry policy moved into the shared `RETRY_POLICIES`
table. **Budget compliance was achieved by removing decision sites, not by splitting files.**

## Key data / numbers

- **Budget dimensions: 4** (files, lines, decision sites, failure-branch ratio).
- **Typical budgets:** simple CRUD **3–4** decision sites; checkout **6–8**; export **6–8**;
  webhook ingest **5–7**; LLM agent **8–10**.
- **Check runtime target: < 10 s** on a 500-file repository; Acme's check runs in **3.2 s**.
- **Failure-branch ratio target: ≤ 0.20** for business logic; Acme's `ExportJob` was **0.36**,
  ended at **0.16**.
- **Quarterly review cadence**, not per-PR: the check runs per PR, the budget review runs
  per quarter.
- **Over-budget features at Acme before the budget: 6 of 14**; after one quarter, **2 of 14**;
  after two quarters, **0**.
- **Effect on review:** feature PRs touching error handling reviewed in **6 min** median
  (was **14 min**), because the reviewer could see the budget diff in the check output.
- **Exception mechanism:** a dated entry in the budget file, **not** an inline comment.
- **Effect on features shipped:** the `export` feature's blocked-release count fell from
  **4 of 9** releases in a quarter to **0 of 11** in the next.

## Real-world use case — Acme SaaS, the feature that ate the roadmap

Acme's `ExportJob` was the reason the export feature slipped in **four consecutive
releases**. Not because of the export itself — because of the error handling around it.

The symptom was always the same: the export feature needed one more failure mode
("the tenant's S3 bucket policy denies writes", "the checkpoint row was written but the
object was not", "the source table was mutated mid-export"), and each one added a branch,
a mapping, a status, and a retry rule. The feature's error-handling surface grew to
**231 lines across 4 files with 14 decision sites** — and every one of those 14 sites had to
be reviewed, understood, and kept in agreement.

The budget was the intervention that made the growth visible. The moment the check was
enabled, the check output for `export` read:

```text
✖ export: 4 error files (max 3)
✖ export: 231 error lines (max 150)
✖ export: 14 decision sites (max 8)
✖ export: failure branch ratio 0.36 (max 0.25)
```

The four lines were more effective than the design document, because they appeared on **every
pull request** and they were numbers. The team could not argue with a number the way they
could argue with a proposal.

The refactor that followed removed **8 of the 14** decision sites and **125** lines. The
feature then shipped on time for the next **11 releases**, and the monthly export incident
count went from **1.7** to **0.3**.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No budget | Zero process | Complexity grows invisibly | Prototypes; projects under 3 months |
| Line budget only | Trivial to compute | Rewards compressed code, not fewer decisions | A first step, with a decision-site budget added later |
| Decision-site budget | Directly measures duplication risk | Needs a definition and a counter | The default for services |
| Per-feature budget | Fair; scaled to the feature's shape | Needs per-feature configuration | Services with several distinct features |
| Global budget | Simple | Punishes legitimate complexity; gets waived | Small services with one feature |
| Review convention, no tool | No setup | Not followed under deadline pressure | Never as the only control |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Budget decision sites first | Budget only lines |
| Set the budget from the feature's shape | Apply one budget to every feature |
| Run the check per PR; review the budget per quarter | Re-negotiate the budget in every PR |
| Lower a budget only after a refactor | Lower a budget to make a failing check pass |
| Record adjustments in the budget file with a date | Waive budgets in chat |
| Raise the budget deliberately, in writing | Let the budget drift upward by neglect |

## Common mistakes

- **The budget becomes a target.** Once a team hits a budget, it stops extracting policies
  even when extraction is clearly right. A budget is a ceiling, not a goal.
- **Counting the wrong thing.** A "decision site" counter that matches `if (err)` counts
  defensive re-throws, not decisions. Agree the definition once.
- **The per-file waiver.** Inline waivers destroy the mechanism within a quarter.
- **Budgeting shared modules by lines.** A shared module's complexity is governed by the
  abstraction cost analysis, not a line count.
- **No quarterly review.** A budget that is never adjusted becomes a fixed point that is
  either ignored or renegotiated at random.

## Checklist

- [ ] Every feature has a budget with a decision-site limit.
- [ ] The budget is derived from the feature's shape, and the derivation is written down.
- [ ] The check runs in under 10 seconds and is part of CI.
- [ ] The check output lists every violated dimension, not just a pass/fail.
- [ ] Adjustments are dated, reasoned, and recorded in the budget file.
- [ ] Budgets are lowered only after a refactor that removed decision sites.

## Related

- [Readable Business Logic and the Easy Path](../01-concepts/05-readable-business-logic-and-the-easy-path.md)
- [Localizing Decisions and Conventions](../01-concepts/04-localizing-decisions-and-conventions.md)
- [Reducing Repetition in the Checkout Flow](./01-reducing-repetition-in-checkout.md)
- [Chapter 52 — Failure-Path Analysis](../../part-20-correctness-and-validation/52-failure-path-analysis/README.md)
